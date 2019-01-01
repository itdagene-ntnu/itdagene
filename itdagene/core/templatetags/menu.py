from django.template import Library

register = Library()


@register.simple_tag
def active(request, pattern):
    import re

    if len(pattern) > 1 and re.search(pattern, request.path):
        return " active "
    elif request.path == "/" and pattern == "/":
        return " active "
    return ""
