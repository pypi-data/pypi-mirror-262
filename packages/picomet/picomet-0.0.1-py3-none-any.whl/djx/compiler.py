import os
import site
import sys
import threading
import time
from hashlib import md5
from pathlib import Path

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.apps import apps
from django.conf import settings
from django.template.loader import get_template
from django.urls import URLPattern, URLResolver, get_resolver
from django.urls.resolvers import RoutePattern

from djx.backends.djx import Renderer
from djx.loaders import fcache
from djx.parser import XTMLParser, cache, compile_sass, dgraph, tw_builds, tw_layouts


def compile():
    package_folders = [
        site.getusersitepackages(),
        *[path for path in site.getsitepackages()],
    ]

    template_folders = [
        os.path.join(settings.BASE_DIR, "xtmls"),
        *[os.path.join(app.path, "xtmls") for app in apps.get_app_configs()],
    ]

    usr_template_folders = template_folders.copy()
    for staticFolder in template_folders:
        for packageFolder in package_folders:
            if Path(staticFolder).is_relative_to(packageFolder):
                if staticFolder in usr_template_folders:
                    usr_template_folders.remove(staticFolder)

    if sys.argv[1] == "runserver":

        def watch(path):
            from watchdog.events import FileSystemEvent, FileSystemEventHandler
            from watchdog.observers import Observer

            class EventHandler(FileSystemEventHandler):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.time = {"modified": {}}

                def dispatch(self, event: FileSystemEvent):
                    src_path: str = event.src_path
                    _, extension = os.path.splitext(src_path)
                    tm = time.time()
                    if (event.event_type == "modified") and (
                        (tm - self.time["modified"].get(src_path, 1.1)) >= 1
                    ):
                        if extension == ".html" and is_file_changed(src_path):
                            self.time["modified"][src_path] = tm

                            parser = XTMLParser()
                            with open(src_path, encoding="utf-8") as f:
                                fcache[src_path] = f.read()
                            parser.feed(fcache[src_path], src_path, use_cache=False)

                            def update(p):
                                for d in dgraph.get(p, []):
                                    parser = XTMLParser()
                                    parser.feed(fcache[d], d, use_cache=False)
                                    update(d)

                            update(src_path)

                            if src_path in tw_layouts.keys():
                                compile_tw(src_path)
                            else:
                                compiled = []

                                def traverse(f: str):
                                    if f in tw_layouts.keys():
                                        if f not in compiled:
                                            compile_tw(f)
                                            compiled.append(f)
                                            send_message(
                                                {
                                                    "tailwind": f"/assets/{tw_builds[f]['fname']}"
                                                }
                                            )

                                    for layout in tw_layouts.keys():
                                        if f in dgraph.get(layout):
                                            if layout not in compiled:
                                                compile_tw(layout)
                                                compiled.append(layout)
                                                send_message(
                                                    {
                                                        "tailwind": f"/assets/{tw_builds[layout]['fname']}"
                                                    }
                                                )
                                    for d in dgraph.get(f, []):
                                        traverse(d)

                                traverse(src_path)

                            send_message(
                                {"layout" if parser.is_layout else "template": src_path}
                            )
                        elif (
                            extension == ".scss"
                            and dgraph.get(src_path)
                            and is_file_changed(src_path)
                        ):
                            self.time["modified"][src_path] = tm
                            compile_sass(src_path)
                            send_message({"style": cache[src_path][0]})
                        elif extension == ".css" and is_file_changed(src_path):
                            self.time["modified"][src_path] = tm
                            for layout in tw_layouts:
                                if src_path == os.path.join(
                                    os.path.dirname(layout),
                                    f"{tw_layouts[layout]}.tw.css",
                                ):
                                    compile_tw(layout)
                                    send_message(
                                        {
                                            "tailwind": f"/assets/{tw_builds[layout]['fname']}"
                                        }
                                    )

            event_handler = EventHandler()
            observer = Observer()
            observer.schedule(event_handler, path, recursive=True)
            observer.start()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
            observer.join()

        def traverse_patterns(url_patterns):
            for url_pattern in url_patterns:
                if isinstance(url_pattern, URLPattern) and isinstance(
                    url_pattern.pattern, RoutePattern
                ):
                    if hasattr(url_pattern.callback, "template_name"):
                        renderer: Renderer = get_template(
                            url_pattern.callback.template_name, using="djx"
                        )
                        html_file = renderer.origin.name
                        with open(html_file) as file:
                            fcache[html_file] = file.read()
                            parser = XTMLParser()
                            parser.feed(fcache[html_file], html_file)
                elif isinstance(url_pattern, URLResolver):
                    traverse_patterns(
                        getattr(
                            url_pattern.urlconf_name,
                            "urlpatterns",
                            url_pattern.urlconf_name,
                        ),
                    )

        traverse_patterns(get_resolver().url_patterns)

        for layout in tw_layouts:
            compile_tw(layout)

        for d in template_folders:
            if os.path.isdir(d):
                if settings.DEBUG:
                    thread = threading.Thread(target=watch, args=(d,), daemon=True)
                    thread.start()


def is_file_changed(path: str):
    f = open(path, encoding="utf-8")
    content = f.read()
    f.close()
    if (not content) or (content == fcache.get(path)):
        return False
    return True


def compile_tw(layout: str):
    source_id = tw_layouts[layout]
    input_css = f"{os.path.dirname(layout)}/{source_id}.tailwind.css"
    tailwind_conf = f"{os.path.dirname(layout)}/{source_id}.tailwind.js"
    postcss_conf = f"{os.path.dirname(layout)}/{source_id}.postcss.js"
    dest_dir: Path = settings.BASE_DIR / ".djx" / "assets"
    if not dest_dir.is_dir():
        dest_dir.mkdir()

    content = []

    def traverse(f: str):
        if f not in content:
            content.append(f)
        for d1 in dgraph:
            for d2 in dgraph[d1]:
                if d2 == f:
                    traverse(d1)

    traverse(layout)

    for f in dgraph[layout]:
        traverse(f)

    from javascript import require

    css, fname = require("./tailwind.js").compile(
        input_css,
        tailwind_conf,
        postcss_conf,
        str(dest_dir),
        f"{source_id}-{md5(layout.encode()).hexdigest()[:6]}",
        content,
    )
    fcache[input_css] = css
    tw_builds[layout] = {"fname": fname}


def send_message(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "hmr",
        {"type": "send.message", "message": message},
    )
