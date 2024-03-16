from collections.abc import Callable
from json import loads

from django.http import HttpRequest, JsonResponse

from djx import call_action
from djx.shortcuts import Redirect


class CommonMiddleware:
    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        request.targets = loads(request.headers.get("Targets", "[]"))

        try:
            call_action(request)
        except Redirect as e:
            return JsonResponse({"redirect": e.args[0], "update": e.args[1]})

        response = self.get_response(request)

        return response
