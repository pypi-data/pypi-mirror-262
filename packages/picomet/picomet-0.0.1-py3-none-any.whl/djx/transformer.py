from copy import copy
from json import dumps, loads
from types import CodeType
from typing import Any, Literal, TypedDict

from django.conf import settings
from django.template.backends.django import Template
from django.utils.html import escape

from djx.parser import cache, tw_builds

try:
    from py_mini_racer import MiniRacer
except ImportError:
    pass

EXCLUDES = ["Outlet", "Fragment", "With", "Defaults", "Children", "Asset"]

type Attrs = list[tuple[str, str | None]]


class Content(TypedDict):
    tag: str | None
    attrs: Attrs
    childrens: list["Content | str | CodeType | Template"] | None
    parent: "Content | None"


type Node = Content | str | CodeType | Template
type Mode = Literal["client", "server"]


class Partial(TypedDict):
    html: str
    css: dict[str, list[str]]
    js: dict[str, list[str]]


class Transformer:
    def __init__(
        self,
        ast: Content,
        context: dict[str, Any],
        targets: list[str],
        keys,
    ):
        self.ast = ast
        self.context = context
        self.ctx = None
        self.targets = targets
        self.keys = keys
        self.content: Content = {
            "tag": None,
            "attrs": [],
            "childrens": [],
            "parent": None,
        }
        self.current: Content = self.content
        self.contents: dict[str, Partial] = {}
        self.c_target: str = ""
        self.assets = {}

    def transform(self):
        self._transform(self.ast)

    def _transform(
        self,
        node: Node,
        xpath="",
        loops=[],
        depth=None,
        previous: bool | None = None,
        mode: Mode = "client",
        file=None,
        **kwargs,
    ):
        if len(self.targets) and not self.c_target:
            if not isinstance(node, dict):
                return
            GROUPS = self.get_attr(node, "s-group", default="").split(",")
            tag = node["tag"]
            if (
                any(f"&{group}" in self.targets for group in GROUPS)
                or ((f"${file}" in self.targets) and tag and (tag not in EXCLUDES))
                or (xpath in self.targets)
            ):
                self.contents[xpath] = {"js": {}, "css": {}, "html": ""}
                self.c_target = xpath
            else:
                mode = self.get_attr(node, "mode", default=mode)
                if mode == "server" and self.ctx is None:
                    self.ctx = MiniRacer()
                attrs = node["attrs"]
                childrens = node.get("childrens", [])
                sfor = self.get_attr(node, "s-for")

                for attr in attrs:
                    k, v = attr
                    if k == "s-data":
                        self.handle_sdata(k, v)
                    elif k.startswith("s-prop:"):
                        self.handle_sprop(k, v, None)
                    elif k == "x-data":
                        self.handle_xdata(k, v, mode)
                if tag == "html" and self.ctx:
                    self.ctx.eval("var isServer = true;")
                store = {}
                if tag == "With":
                    self.pack_with(attrs, store)
                if sfor:
                    self.handle_sfor(
                        node,
                        childrens,
                        xpath=xpath,
                        loops=loops,
                        depth=depth,
                        mode=mode,
                        file=file,
                        **kwargs,
                    )
                else:
                    self.loop(
                        childrens,
                        xpath=xpath,
                        loops=loops,
                        depth=depth,
                        mode=mode,
                        file=file,
                        **kwargs,
                    )
                self.unpack_store(store)
                return

        if isinstance(node, str):
            if self.c_target:
                self.contents[self.c_target]["html"] += node
            else:
                self.current["childrens"].append(node)
            return
        elif isinstance(node, CodeType):
            if self.c_target:
                self.contents[self.c_target]["html"] += str(eval(node, self.context))
            else:
                self.current["childrens"].append(str(eval(node, self.context)))
            return
        elif isinstance(node, Template):
            if self.c_target:
                self.contents[self.c_target]["html"] += node.render(self.context)
            else:
                self.current["childrens"].append(node.render(self.context))
            return

        mode = self.get_attr(node, "mode", default=mode)
        if mode == "server" and self.ctx is None:
            self.ctx = MiniRacer()
        tag = node["tag"]
        attrs = []
        childrens = node.get("childrens")
        text = None
        sfor = self.get_attr(node, "s-for")

        show = self.get_attr(node, "s-show")
        if show and not eval(show, self.context):
            if self.c_target:
                self.contents[self.c_target]["html"] += f"<{tag} hidden></{tag}>"
                if xpath == self.c_target and tag and (tag not in EXCLUDES):
                    self.c_target = ""
            else:
                self.current["childrens"].append(
                    {
                        "tag": tag,
                        "attrs": [("hidden", None)],
                        "childrens": [],
                        "parent": self.current,
                    }
                )
            return False
        elif self.get_attr(node, "s-if") and not eval(
            self.get_attr(node, "s-if"), self.context
        ):
            return False
        elif self.get_attr(node, "s-elif"):
            if previous is True:
                return True
            elif not eval(self.get_attr(node, "s-elif"), self.context):
                return False
        elif self.get_attr(node, "s-else") is None and previous is True:
            return
        elif self.get_attr(node, "s-empty") is None and previous is True:
            return

        for attr in node["attrs"]:
            k, _ = attr
            if not k.startswith("x-") and not k.startswith("s-") and k != "mode":
                attrs.append(attr)

        for attr in node["attrs"]:
            k, v = attr
            if k == "s-data":
                self.handle_sdata(k, v)
            elif k.startswith("s-prop:"):
                self.handle_sprop(k, v, attrs)
            elif k == "x-data":
                self.handle_xdata(k, v, mode)
                attrs.append(attr)
            elif k == "x-show":
                if mode == "server" and self.ctx and not self.ctx.eval(v):
                    styles = self.get_attr(attrs, "style", default="").split(";")
                    styles.append("display:none!important")
                    self.set_attr(attrs, "style", ";".join(styles))
                attrs.append(attr)
            elif k == "s-text":
                text = escape(eval(v, self.context))
            elif k == "x-text":
                if mode == "server" and self.ctx:
                    text = escape(self.ctx.eval(v))
                attrs.append(attr)
            elif k.startswith("s-bind:"):
                if k.split(":")[1] == "class":
                    self.set_attr(
                        attrs,
                        "class",
                        self.add_classes(
                            self.get_attr(attrs, "class", default=""),
                            [escape(eval(v, self.context))],
                        ),
                    )
                else:
                    value = eval(v, self.context)
                    if k.split(":")[1] == "x-prop":
                        value = dumps(value)
                    attrs.append((":".join(k.split(":")[1:]), escape(value)))
            elif k.startswith("s-toggle:"):
                val = eval(v, self.context)
                if val is True:
                    attrs.append((":".join(k.split(":")[1:]), None))
            elif k.startswith("x-bind:"):
                attrs.append(attr)
                if mode == "server" and self.ctx:
                    if k.split(":")[1] == "class":
                        if v.startswith("{"):
                            self.ctx.eval(
                                f"var classes = {v}; var klasses = []; for (let k in classes) {{ if (classes[k]) {{klasses.push(k)}} }};"
                            )
                            self.set_attr(
                                attrs,
                                "class",
                                self.add_classes(
                                    self.get_attr(attrs, "class", default=""),
                                    loads(self.ctx.eval("JSON.stringify(klasses)")),
                                ),
                            )
                        else:
                            self.set_attr(attrs, "class", escape(self.ctx.eval(v)))
                    else:
                        val = self.ctx.eval(v)
                        if val is not False:
                            attrs.append((k.split(":")[1], escape(val)))
            elif k == "s-k":
                attrs.append(("k", escape(loops[-1][1])))
                attrs.append(("x-prop:keys", escape(dumps(loops))))
            elif k.startswith("s-asset:"):
                attrs.append((k.split(":")[1], f"/assets/{cache.get(v)[0]}"))
            elif k.startswith("s-static:"):
                attrs.append((k.split(":")[1], escape(settings.STATIC_URL + v)))
            elif k.startswith("x-"):
                attrs.append(attr)

        store = {}
        if tag == "With":
            self.pack_with(attrs, store)

        if tag == "Defaults":
            for k, v in attrs:
                if not self.context.get(k):
                    store[k] = self.context.get(k)
                    self.context[k] = eval(v, self.context)

        if tag == "html" and self.ctx:
            self.ctx.eval("var isServer = true;")
            attrs.append(("x-data", "{isServer: false, keys: []}"))

        if self.c_target:
            if tag == "Sass":
                fname = self.get_attr(node, "#")
                asset_id = cache.get(fname)[0].split(".")[1]
                if not self.contents[self.c_target]["css"].get(asset_id):
                    self.contents[self.c_target]["css"][
                        asset_id
                    ] = f"/assets/{cache.get(fname)[0]}"
            else:
                attributes = self.join_attrs(attrs)
                if isinstance(childrens, list):
                    if tag and (tag not in EXCLUDES):
                        self.contents[self.c_target]["html"] += f"<{tag}{attributes}>"
                    if sfor:
                        if not self.handle_sfor(
                            node,
                            childrens,
                            xpath=xpath,
                            loops=loops,
                            depth=depth,
                            mode=mode,
                            **kwargs,
                        ):
                            self.unpack_store(store)
                            return False
                    elif text:
                        self.contents[self.c_target]["html"] += text
                    else:
                        self.loop(
                            childrens,
                            xpath=xpath,
                            loops=loops,
                            depth=depth,
                            mode=mode,
                            **kwargs,
                        )
                    if tag and (tag not in EXCLUDES):
                        self.contents[self.c_target]["html"] += f"</{tag}>"

                    if xpath == self.c_target and tag and (tag not in EXCLUDES):
                        self.c_target = ""
                else:
                    self.contents[self.c_target]["html"] += f"<{tag}{attributes} />"
        elif tag == "Sass":
            fname = self.get_attr(node, "#")
            asset_id = cache.get(fname)[0].split(".")[0]
            assets = self.assets[self.get_attr(node, "group")]["childrens"]
            exists = False
            for asset in assets:
                if self.get_attr(asset, "id") == asset_id:
                    exists = True
            if not exists:
                assets.append(
                    {
                        "tag": "style",
                        "attrs": [("id", asset_id)],
                        "childrens": [cache.get(fname)[1]],
                    }
                )
        elif tag == "Tailwind":
            fname = tw_builds[self.get_attr(node, "layout")]["fname"]
            self.current["childrens"].append(
                {
                    "tag": "link",
                    "attrs": [
                        ("rel", "stylesheet"),
                        ("href", f"/assets/{fname}"),
                        ("id", "tw"),
                    ],
                }
            )
        else:
            element = {"tag": tag, "attrs": attrs, "parent": self.current}
            self.current["childrens"].append(element)
            if tag == "Asset":
                self.assets[self.get_attr(node, "name")] = element
            self.current = element
            if isinstance(childrens, list):
                element["childrens"] = []
                if sfor:
                    if not self.handle_sfor(
                        node,
                        childrens,
                        xpath=xpath,
                        loops=loops,
                        depth=depth,
                        mode=mode,
                        **kwargs,
                    ):
                        self.unpack_store(store)
                        return False
                elif text:
                    element["childrens"].append(text)
                else:
                    self.loop(
                        childrens,
                        xpath=xpath,
                        loops=loops,
                        depth=depth,
                        mode=mode,
                        **kwargs,
                    )
            self.current = element["parent"]

        self.unpack_store(store)
        return True

    def loop(self, childrens: list[Node], **kwargs):
        previous = None
        xpath = kwargs.pop("xpath")
        file = kwargs.get("file")
        kwargs["depth"] = 0 if kwargs["depth"] is None else kwargs["depth"] + 1

        el_index = {} if kwargs.get("el_index") is None else kwargs.get("el_index")
        for index, children in enumerate(childrens):
            _xpath = copy(xpath)
            if isinstance(children, dict):
                tag = children["tag"]
                _file = children.get("file") or file
                kwargs["file"] = _file
                if tag and (tag not in EXCLUDES):
                    el_index.setdefault(tag, 0)
                    el_index[tag] += 1
                    k = self.get_attr(children, "s-k")
                    _index = (
                        f"@k={kwargs['loops'][-1][1]}" if k is None else el_index[tag]
                    )
                    _xpath += f"/{tag}[{_index}]"
                    kwargs["el_index"] = None
                else:
                    kwargs["el_index"] = el_index
                if (
                    len(self.targets)
                    and not self.c_target
                    and (
                        not (
                            self.is_required(kwargs["depth"], index, _xpath)
                            or (f"${_file}" in self.targets)
                        )
                    )
                ):
                    if isinstance(kwargs.get("el_index"), dict):

                        def traverse(node: Content):
                            for children in node.get("childrens", []):
                                if isinstance(children, dict):
                                    tag = children["tag"]
                                    if tag and (tag not in EXCLUDES):
                                        el_index.setdefault(tag, 0)
                                        el_index[tag] += 1
                                    else:
                                        traverse(children)

                        traverse(children)
                    continue
            _return = self._transform(
                node=children, xpath=_xpath, previous=previous, **kwargs
            )
            previous = _return if isinstance(children, dict) else previous

    def handle_sprop(self, k: str, v: str | CodeType, attrs):
        prop = escape(k.split(":")[1])
        value = dumps(eval(v, self.context))
        self.ctx.eval(f"var {prop} = JSON.parse('{value.replace("'","\\'")}');")
        if isinstance(attrs, list):
            attrs.append((f"x-prop:{prop}", escape(value)))

    def handle_sdata(self, k: str, v: str | CodeType):
        datas = eval(v)
        for data in datas:
            self.context[data] = datas[data]

    def handle_xdata(self, k: str, v: str, mode: str):
        if mode == "server" and v.strip().startswith("{") and self.ctx:
            self.ctx.eval(
                f"var data = {v}; for (let k in data) {{ globalThis[k] = data[k] }};"
            )

    def handle_sfor(self, node: Content, childrens, **kwargs):
        _item = self.get_attr(node, "s-for")
        _key = self.get_attr(node, "s-key")
        array: list = None
        for key in self.keys:
            if kwargs["xpath"] == key[0]:
                array = eval(self.get_attr(node, "s-of"), self.context, {"key": key[1]})
        if not array:
            array = eval(self.get_attr(node, "s-in"), self.context)
        el_index = {}
        kwargs["el_index"] = el_index

        outer = self.context.get(_item)
        for index, item in enumerate(array):
            self.context[_item] = item
            self.context["index"] = index
            loops = [
                *kwargs["loops"],
                [kwargs["xpath"], eval(_key, self.context)],
            ]
            kwargs["loops"] = loops
            self.loop(childrens, **kwargs)
        self.context[_item] = outer
        if len(array):
            return True

    def pack_with(self, attrs, store: dict[str, Any]):
        for k, v in attrs:
            store[k] = self.context.get(k)
            self.context[k] = eval(v, self.context)

    def unpack_store(self, store: dict[str, Any]):
        for k in store:
            self.context[k] = store[k]

    def get_attr[T](self, obj: Content | Attrs, name: str, default: T = False):
        attrs = []
        if isinstance(obj, dict):
            attrs = obj["attrs"]
        elif isinstance(obj, list):
            attrs = obj
        return next(filter(lambda attr: attr[0] == name, attrs), [name, default])[1]

    def set_attr(self, attrs: Attrs, name: str, value: str | None):
        for index, attr in enumerate(attrs):
            if attr[0] == name:
                attrs[index] = (name, value)
                return
        attrs.append((name, value))

    def add_classes(self, string: str, classes):
        klasses = string.strip().split(" ")
        for klass in classes:
            if klass and klass not in klasses:
                klasses.append(klass)
        return " ".join(klasses)

    def join_attrs(self, attrs: Attrs):
        return "".join(
            map(
                lambda attr: f' {attr[0]}="{attr[1]}"' if attr[1] else f" {attr[0]}",
                attrs,
            )
        )

    def is_required(self, depth: int, index: int, xpath: str):
        for target in self.targets:
            if target.startswith("$"):
                for loc in self.ast["map"]["files"].get(target[1:], []):
                    if len(loc) > depth and loc[depth] == index:
                        return True
            elif target.startswith("&"):
                for loc in self.ast["map"]["groups"].get(target[1:], []):
                    if len(loc) > depth and loc[depth] == index:
                        return True
            elif target.startswith("/"):
                if target.startswith(xpath):
                    return True
        return False

    def compile_content(self):
        def compile(node: Content | str):
            compiled = ""
            if not isinstance(node, dict):
                compiled += str(node)
            else:
                tag = node["tag"]
                childrens = node.get("childrens")
                attributes = self.join_attrs(node["attrs"])
                if isinstance(childrens, list):
                    if tag and (tag not in EXCLUDES):
                        compiled += f"<{tag}{attributes}>"
                    for children in childrens:
                        compiled += compile(children)
                    if tag and (tag not in EXCLUDES):
                        compiled += f"</{tag}>"
                else:
                    compiled += f"<{tag}{attributes} />"
            return compiled

        return compile(self.content)
