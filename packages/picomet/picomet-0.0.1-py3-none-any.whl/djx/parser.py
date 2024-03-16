import functools
import os
import re
from copy import deepcopy
from glob import glob
from hashlib import md5
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from types import CodeType
from typing import override

from django.apps import apps
from django.conf import settings
from django.template import engines, loader

django_engine = engines["django"]

cache = {}

dgraph: dict[str, list[str]] = {}

tw_layouts = {}

tw_builds = {}

djx_dir: Path = settings.BASE_DIR / ".djx"
assets_dir: Path = djx_dir / "assets"
if not djx_dir.is_dir():
    djx_dir.mkdir()
if not assets_dir.is_dir():
    assets_dir.mkdir()

tagfind_tolerant = re.compile(r"([a-zA-Z][^\t\n\r\f />\x00]*)(?:\s|/(?!>))*")
attrfind_tolerant = re.compile(
    r'((?<=[\'"\s/])[^\s/>][^\s/=>]*)(\s*=+\s*'
    r'(\'[^\']*\'|"[^"]*"|(?![\'"])[^>\s]*))?(?:\s|/(?!>))*'
)
endendtag = re.compile(">")
endtagfind = re.compile(r"</\s*([a-zA-Z][-.a-zA-Z0-9:_]*)\s*>")


class BaseHTMLParser(HTMLParser):
    # Internal -- handle starttag, return end or -1 if not terminated
    @override
    def parse_starttag(self, i):
        self.__starttag_text = None
        endpos = self.check_for_whole_start_tag(i)
        if endpos < 0:
            return endpos
        rawdata = self.rawdata
        self.__starttag_text = rawdata[i:endpos]

        # Now parse the data between i+1 and j into a tag and attrs
        attrs = []
        match = tagfind_tolerant.match(rawdata, i + 1)
        assert match, "unexpected call to parse_starttag()"
        k = match.end()
        self.lasttag = tag = match.group(1)
        while k < endpos:
            m = attrfind_tolerant.match(rawdata, k)
            if not m:
                break
            attrname, rest, attrvalue = m.group(1, 2, 3)
            if not rest:
                attrvalue = None
            elif (
                attrvalue[:1] == "'" == attrvalue[-1:]
                or attrvalue[:1] == '"' == attrvalue[-1:]
            ):
                attrvalue = attrvalue[1:-1]
            if attrvalue:
                attrvalue = unescape(attrvalue)
            attrs.append((attrname, attrvalue))
            k = m.end()

        end = rawdata[k:endpos].strip()
        if end not in (">", "/>"):
            lineno, offset = self.getpos()
            if "\n" in self.__starttag_text:
                lineno = lineno + self.__starttag_text.count("\n")
                offset = len(self.__starttag_text) - self.__starttag_text.rfind("\n")
            else:
                offset = offset + len(self.__starttag_text)
            self.handle_data(rawdata[i:endpos])
            return endpos
        if end.endswith("/>"):
            # XHTML-style empty tag: <span attr="value" />
            self.handle_startendtag(tag, attrs)
        else:
            self.handle_starttag(tag, attrs)
            if tag in self.CDATA_CONTENT_ELEMENTS:
                self.set_cdata_mode(tag)
        return endpos

    # Internal -- parse endtag, return end or -1 if incomplete
    @override
    def parse_endtag(self, i):
        rawdata = self.rawdata
        assert rawdata[i : i + 2] == "</", "unexpected call to parse_endtag"
        match = endendtag.search(rawdata, i + 1)  # >
        if not match:
            return -1
        gtpos = match.end()
        match = endtagfind.match(rawdata, i)  # </ + tag + >
        if not match:
            if self.cdata_elem is not None:
                self.handle_data(rawdata[i:gtpos])
                return gtpos
            # find the name: w3.org/TR/html5/tokenization.html#tag-name-state
            namematch = tagfind_tolerant.match(rawdata, i + 2)
            if not namematch:
                # w3.org/TR/html5/tokenization.html#end-tag-open-state
                if rawdata[i : i + 3] == "</>":
                    return i + 3
                else:
                    return self.parse_bogus_comment(i)
            tagname = namematch.group(1)
            # consume and ignore other stuff between the name and the >
            # Note: this is not 100% correct, since we might have things like
            # </tag attr=">">, but looking for > after the name should cover
            # most of the cases and is much simpler
            gtpos = rawdata.find(">", namematch.end())
            self.handle_endtag(tagname)
            return gtpos + 1

        elem = match.group(1)  # script or style
        if self.cdata_elem is not None:
            if elem != self.cdata_elem:
                self.handle_data(rawdata[i:gtpos])
                return gtpos

        self.handle_endtag(elem)
        self.clear_cdata_mode()
        return gtpos


trim_re = re.compile(r"(^(\s|\n|\t)+|(\s|\n|\t)+$)")

x_re = re.compile(
    r"(?:(?:({\$)\s*((?:\"(?:\\\"|[^\"])*\"|'(?:\\'|[^'])*'|[^\"'\n])*?)\s*\$})|(({{)\s*((?:\"(?:\\\"|[^\"])*\"|'(?:\\'|[^'])*'|[^\"'\n])*?)\s*}})|({%\s*((?:\"(?:\\\"|[^\"])*\"|'(?:\\'|[^'])*'|[^\"'\n])*?)\s*%}))"
)

type Attrs = list[tuple[str, str | None]]


class XTMLParser(BaseHTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ast = {
            "tag": None,
            "attrs": [],
            "childrens": [],
            "parent": None,
            "map": {"groups": {}, "files": {}},
        }
        self.imports: dict[str, str] = {}
        self.loc: list[int] = []
        self.current = self.ast
        self.is_layout: bool = False
        self.is_page: bool = False
        self.in_layout: bool = False
        self.in_debug: bool = False

    def feed(self, data: str, id: str, use_cache: bool = True):
        self.id = id
        cached = cache.get(id)
        if use_cache:
            if not cached:
                self.ast["file"] = id
                self.ast["map"]["files"].setdefault(id, [[]])
                super().feed(data)
                cache[id] = self.ast
            else:
                self.ast = cached
        else:
            self.ast["file"] = id
            self.ast["map"]["files"].setdefault(id, [[]])
            super().feed(data)
            cache[id] = self.ast

    def handle_addition(func):
        @functools.wraps(func)
        def wrapper(self, *args):
            if self.in_debug and not settings.DEBUG:
                return
            if self.is_page and not self.in_layout:
                return
            func(self, *args)

        return wrapper

    @handle_addition
    def handle_starttag(self, tag, attrs):
        if tag == "Debug":
            self.in_debug = True
        elif (
            tag == "Layout"
            and self.current is self.ast
            and not len(self.ast["childrens"])
        ):
            self.is_page = True
            self.in_layout = True
            component = self.get_attr(attrs, "#")
            if len(os.path.basename(component).split(".")) == 1:
                component = f"{component}.html"
            template = loader.get_template(component, using="djx").template
            parser = XTMLParser()
            id = template.origin.name
            parser.feed(template.source, id)
            self.add_dep(id, self.id)
            ast = deepcopy(self.ast)
            self.ast = deepcopy(parser.ast)
            loc = self.find_loc("Outlet", self.ast, [])
            if loc:
                el = self.ast
                for _loc in loc:
                    el = el["childrens"][_loc]
                el["childrens"].append(ast)
                self.loc = loc + [0]
                for file in ast["map"]["files"]:
                    for _loc in ast["map"]["files"][file]:
                        self.ast["map"]["files"].setdefault(file, [])
                        self.ast["map"]["files"][file].append(self.loc + _loc)
                self.current = ast
        elif (
            self.imports.get(tag[:-1])
            or engines["djx"].engine.components.get(tag[:-1])
            or (tag == "Include")
        ):
            component = (
                self.imports.get(tag[:-1])
                or engines["djx"].engine.components.get(tag[:-1])
                or self.get_attr(attrs, "#")
            )
            if component:
                if len(os.path.basename(component).split(".")) == 1:
                    component = f"{component}.html"
                template = loader.get_template(component, using="djx").template
                parser = XTMLParser()
                id = template.origin.name
                parser.feed(template.source, id)
                ast = deepcopy(parser.ast)
                self.add_props(
                    ast,
                    self.process_attrs(
                        [(k, v) for k, v in attrs if k != "#" and not k.startswith(".")]
                    ),
                )
                self.add_dep(id, self.id)
                self.current["childrens"].append(
                    {
                        "tag": "With",
                        "attrs": self.withs(
                            [(k[1:], v) for k, v in attrs if k.startswith(".")]
                        ),
                        "childrens": [ast],
                        "parent": self.current,
                    }
                )
                ast["parent"] = self.current["childrens"][-1]
                self.load_map(ast["map"])

                self.loc = (
                    self.loc
                    + [len(self.current["childrens"]), 0]
                    + self.find_loc("Children", ast, [])
                )
                self.current = self.find_node(
                    "Children", self.current["childrens"][-1], []
                )
        else:
            if tag == "With":
                attributes = self.withs(attrs)
            else:
                attributes = self.process_attrs(attrs)
            self.loc.append(len(self.current["childrens"]))
            self.current["childrens"].append(
                {
                    "tag": tag,
                    "attrs": attributes,
                    "childrens": [],
                    "parent": self.current,
                }
            )
            self.current = self.current["childrens"][-1]
            sgroup = self.get_attr(attributes, "s-group")
            if sgroup:
                for group in sgroup.split(","):
                    self.ast["map"]["groups"].setdefault(group, [])
                    self.ast["map"]["groups"][group].append(self.loc.copy())

    @handle_addition
    def handle_startendtag(self, tag, attrs):
        if tag.startswith("Import."):
            component = self.get_attr(attrs, "#")
            if component:
                self.imports[f"{tag[7:]}"] = component
        elif tag == "Outlet":
            self.current["childrens"].append(
                {"tag": tag, "attrs": attrs, "childrens": [], "parent": self.current}
            )
        elif tag == "Children":
            self.current["childrens"].append(
                {"tag": tag, "attrs": attrs, "childrens": [], "parent": self.current}
            )
        elif (
            self.imports.get(tag[:-1])
            or engines["djx"].engine.components.get(tag[:-1])
            or (tag == "Include")
        ):
            component = (
                self.imports.get(tag[:-1])
                or engines["djx"].engine.components.get(tag[:-1])
                or self.get_attr(attrs, "#")
            )
            if component:
                if len(os.path.basename(component).split(".")) == 1:
                    component = f"{component}.html"
                template = loader.get_template(component, using="djx").template
                parser = XTMLParser()
                id = template.origin.name
                parser.feed(template.source, id)
                ast = deepcopy(parser.ast)
                self.add_dep(id, self.id)
                self.add_props(
                    ast,
                    self.process_attrs(
                        [(k, v) for k, v in attrs if k != "#" and not k.startswith(".")]
                    ),
                )
                self.current["childrens"].append(
                    {
                        "tag": "With",
                        "attrs": self.withs(
                            [(k[1:], v) for k, v in attrs if k.startswith(".")]
                        ),
                        "childrens": [ast],
                        "parent": self.current,
                    }
                )
                ast["parent"] = self.current["childrens"][-1]
                self.load_map(ast["map"])
        elif tag == "Asset":
            self.current["childrens"].append(
                {
                    "tag": tag,
                    "attrs": attrs,
                    "childrens": [],
                    "parent": self.current,
                }
            )
        elif tag == "Sass":
            component = self.get_attr(attrs, "#")
            id = os.path.join(os.path.dirname(self.id), component)
            self.add_dep(id, self.id)
            attrs[0] = ("#", id)
            self.current["childrens"].append(
                {
                    "tag": tag,
                    "attrs": attrs,
                    "parent": self.current,
                }
            )

            if not cache.get(id):
                compile_sass(id)
        elif tag == "Tailwind":
            if self.current["tag"] == "head":
                tw_layouts[self.id] = self.get_attr(attrs, "#")
                self.current["childrens"].append(
                    {
                        "tag": tag,
                        "attrs": [*attrs, ("layout", self.id)],
                        "parent": self.current,
                    }
                )
        else:
            attributes = self.process_attrs(attrs)
            self.current["childrens"].append(
                {"tag": tag, "attrs": attributes, "parrent": self.current}
            )
            sgroup = self.get_attr(attributes, "s-group")
            if sgroup:
                for group in sgroup.split(","):
                    self.ast["map"]["groups"].setdefault(group, [])
                    self.ast["map"]["groups"][group].append(
                        self.loc.copy() + [len(self.current["childrens"])]
                    )

    def handle_endtag(self, tag):
        if self.in_debug:
            if tag == "Debug":
                self.in_debug = False
                return
            elif not settings.DEBUG:
                return

        if tag == "Layout":
            self.in_layout = False
        elif (
            self.imports.get(tag[:-1])
            or engines["djx"].engine.components.get(tag[:-1])
            or (tag == "Include")
        ):
            while True:
                if self.current["tag"] == "With":
                    break
                else:
                    if len(self.loc):
                        self.loc.pop(-1)
                    self.current = self.current["parent"]
        if len(self.loc):
            self.loc.pop(-1)
        self.current = self.current["parent"]

    @handle_addition
    def handle_data(self, data):
        if not settings.DEBUG:
            data = re.sub(trim_re, "", data)
        matches = list(re.finditer(x_re, data))
        if not len(matches):
            self.current["childrens"].append(data)
        previous = None
        for match in matches:
            self.current["childrens"].append(
                data[previous if previous else 0 : match.start()]
            )
            groups = [group for group in (match.groups()) if group is not None]
            if groups[0] == "{$":
                self.current["childrens"].append(compile(groups[1], self.id, "eval"))
            elif groups[1] == "{{" or groups[1] == "{%":
                self.current["childrens"].append(django_engine.from_string(groups[0]))
            previous = match.end()
        if previous:
            self.current["childrens"].append(data[previous:])

    def handle_decl(self, decl):
        self.is_layout = True
        self.current["childrens"].append(f"<!{decl}>")

    def handle_charref(self, name):
        print("Encountered a charref  :", name)

    def handle_entityref(self, name):
        print("Encountered an entityref  :", name)

    def handle_pi(self, data):
        print("Encountered a pi  :", data)

    def process_attrs(self, attrs: Attrs):
        attributes: list[tuple[str, str | None | CodeType]] = []
        for k, v in attrs:
            if (
                k == "s-show"
                or k == "s-if"
                or k == "s-elif"
                or k == "s-in"
                or k == "s-of"
                or k == "s-key"
                or k == "s-text"
                or k.startswith("s-bind:")
                or k.startswith("s-toggle:")
                or k.startswith("s-prop:")
            ):
                attributes.append((k, self.compile(v)))
            elif k.startswith("s-asset:"):
                for app in apps.get_app_configs():
                    assets_dir = Path(app.path) / "assets"
                    if assets_dir.is_dir() and isinstance(v, str):
                        asset = assets_dir / v
                        if asset.exists():
                            compile_asset(asset.as_posix())
                            attributes += [
                                (k, asset.as_posix()),
                                ("id", md5(asset.as_posix().encode()).hexdigest()[:6]),
                                ("target", k.split(":")[1]),
                            ]
            elif k == "server" or k == "client":
                attributes.append(("mode", k))
            else:
                attributes.append((k, v))

        return attributes

    def compile(self, v: str):
        return compile(v, self.id, mode="eval")

    def withs(self, attrs: Attrs):
        _withs: list[tuple[str, CodeType]] = []
        for k, v in attrs:
            _withs.append(
                (
                    k,
                    self.compile("True") if v is None else self.compile(v),
                )
            )
        return _withs

    def get_attr[T](self, attrs: Attrs, name: str, default: T = None):
        return next(filter(lambda attr: attr[0] == name, attrs), (name, default))[1]

    def add_props(self, ast, props: Attrs):
        if isinstance(ast, dict):
            for index, attr in enumerate(ast["attrs"]):
                if attr[0] == "props":
                    ast["attrs"] = tuple(
                        list(ast["attrs"])[:index]
                        + list(props)
                        + list(ast["attrs"])[index + 1 :]
                    )
            for children in ast.get("childrens", []):
                self.add_props(children, props)

    def add_dep(self, component: str, dependent: str):
        dgraph.setdefault(component, [])
        if dependent not in dgraph[component]:
            dgraph[component].append(dependent)

    def find_loc(self, tag: str, ast, attrs: Attrs, loc=None):
        loc = loc or []
        if isinstance(ast, dict):
            if ast.get("tag") == tag:
                for attr in attrs:
                    if not (self.get_attr(ast["attrs"], attr[0]) == attr[1]):
                        break
                else:
                    return loc
            for index, children in enumerate(ast.get("childrens", [])):
                loc.append(index)
                _loc = self.find_loc(tag, children, attrs, loc=loc)
                if _loc:
                    return _loc
                loc.pop(-1)

    def find_node(self, tag: str, ast, attrs: Attrs):
        if isinstance(ast, dict):
            if ast.get("tag") == tag:
                for attr in attrs:
                    if not (self.get_attr(ast["attrs"], attr[0]) == attr[1]):
                        break
                else:
                    return ast
            for children in ast.get("childrens", []):
                node = self.find_node(tag, children, attrs)
                if node:
                    return node

    def load_map(self, map):
        groups = map["groups"]
        for file in groups:
            self.ast["map"]["groups"].setdefault(file, [])
            self.ast["map"]["groups"][file] += list(
                [
                    (self.loc + [len(self.current["childrens"]) - 1, 0] + _loc)
                    for _loc in groups[file]
                ]
            )
        files = map["files"]
        for file in files:
            self.ast["map"]["files"].setdefault(file, [])
            self.ast["map"]["files"][file] += list(
                [
                    (self.loc + [len(self.current["childrens"]) - 1, 0] + _loc)
                    for _loc in files[file]
                ]
            )


def compile_asset(path: str):
    f = open(path)
    content = f.read()
    from djx.loaders import fcache

    fcache[path] = content
    f.close()
    compiled = content
    name, ext = os.path.splitext(os.path.basename(path))
    id = f"{name}-{md5(path.encode()).hexdigest()[:6]}"
    fname = f"{id}.{md5(compiled.encode()).hexdigest()[:6]}{ext}"
    cache[path] = (fname, compiled)
    for f in glob(str(assets_dir / f"{id}.*{ext}")):
        if os.path.exists(f):
            os.remove(f)
    with open(assets_dir / fname, "w") as f:
        f.write(compiled)


load_paths = [
    os.path.join(settings.BASE_DIR, "assets"),
    *[os.path.join(app.path, "assets") for app in apps.get_app_configs()],
]


def compile_sass(path: str):
    f = open(path)
    content = f.read()
    from djx.loaders import fcache

    fcache[path] = content
    f.close()
    from javascript import require

    compiled: str = (
        require("sass")
        .compileString(
            content,
            {
                "loadPaths": load_paths,
                "style": "expanded" if settings.DEBUG else "compressed",
            },
        )
        .css
    )
    id = f"{os.path.splitext(os.path.basename(path))[0]}-{md5(path.encode()).hexdigest()[:6]}"
    fname = f"{id}.{md5(compiled.encode()).hexdigest()[:6]}.css"
    cache[path] = (fname, compiled)
    for f in glob(str(assets_dir / f"{id}.*.css")):
        if os.path.exists(f):
            os.remove(f)
    with open(assets_dir / fname, "w") as f:
        f.write(compiled)
