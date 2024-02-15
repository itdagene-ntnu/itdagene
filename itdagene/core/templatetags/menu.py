import re

from django.http import HttpRequest
from django.template import Library

register = Library()


@register.simple_tag
def active(request: HttpRequest, pattern: str) -> str:
    if len(pattern) > 1 and re.search(pattern, request.path):
        return " active "
    elif request.path == "/" and pattern == "/":
        return " active "
    return ""


@register.simple_tag
def menu_open(request: HttpRequest, pattern: str) -> str:
    if len(pattern) > 1 and re.search(pattern, request.path):
        return " menu-open "
    return ""
