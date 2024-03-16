from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.template import loader

from djx.backends.djx import Renderer


def page(
    request: HttpRequest,
    context: dict[str, Any] = {},
    content_type: str = None,
    status: int = None,
):
    template: Renderer = loader.get_template(request.template_name, using="djx")
    content = template.render(context, request)
    if isinstance(content, dict):
        return JsonResponse(content, content_type, status)
    return HttpResponse(content, content_type, status)
