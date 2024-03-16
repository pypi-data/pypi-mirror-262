import functools
from collections.abc import Callable

from django.http import HttpRequest


def template(template_name: str):
    def deco(function: Callable):
        function.template_name = template_name

        @functools.wraps(function)
        def wrapper(request: HttpRequest, *args, **kwargs):
            request.template_name = template_name
            return function(request, *args, **kwargs)

        return wrapper

    return deco
