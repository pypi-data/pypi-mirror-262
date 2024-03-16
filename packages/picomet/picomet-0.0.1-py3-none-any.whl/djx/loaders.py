from django.core.exceptions import SuspiciousFileOperation
from django.template import Origin, TemplateDoesNotExist
from django.template.loaders.base import Loader
from django.template.utils import get_app_template_dirs
from django.utils._os import safe_join

from djx.backends.djx import Template

fcache = {}


class BaseLoader(Loader):
    def get_template(self, template_name, skip=None):
        """
        Call self.get_template_sources() and return a Template object for
        the first template matching template_name. If skip is provided, ignore
        template origins in skip. This is used to avoid recursion during
        template extending.
        """
        tried = []

        origin: Origin

        for origin in self.get_template_sources(template_name):
            if skip is not None and origin in skip:
                tried.append((origin, "Skipped to avoid recursion"))
                continue

            try:
                contents = self.get_contents(origin)
            except TemplateDoesNotExist:
                tried.append((origin, "Source does not exist"))
                continue
            else:
                return Template(
                    contents,
                    origin,
                    origin.template_name,
                    self.engine,
                )

        raise TemplateDoesNotExist(template_name, tried=tried)


class FilesystemLoader(BaseLoader):
    def __init__(self, engine):
        super().__init__(engine)

    def get_dirs(self):
        return self.engine.dirs

    def get_contents(self, origin: Origin):
        try:
            cached = fcache.get(origin.name)
            if not cached:
                with open(origin.name, encoding=self.engine.file_charset) as fp:
                    fcache[origin.name] = fp.read()
                    return fcache[origin.name]
            return cached
        except FileNotFoundError:
            raise TemplateDoesNotExist(origin)

    def get_template_sources(self, template_name):
        """
        Return an Origin object pointing to an absolute path in each directory
        in template_dirs. For security reasons, if a path doesn't lie inside
        one of the template_dirs it is excluded from the result set.
        """
        for template_dir in self.get_dirs():
            try:
                name = safe_join(template_dir, template_name)
            except SuspiciousFileOperation:
                # The joined path was located outside of this template_dir
                # (it might be inside another one, so this isn't fatal).
                continue

            yield Origin(
                name=name,
                template_name=template_name,
                loader=self,
            )


class AppdirLoader(FilesystemLoader):
    def get_dirs(self):
        return get_app_template_dirs("xtmls")
