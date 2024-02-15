from datetime import date
from typing import Any

from django.conf import settings
from django.template import Library
from django.template.loader import get_template
from django.utils import timezone
from django.utils.safestring import mark_safe

register = Library()


@register.simple_tag
def analytics() -> str:
    """Find the analytics id from the settingsfile, if debug is false"""
    analytics_id = settings.SITE["analytics"]
    domain = settings.SITE["domain"]
    if not settings.DEBUG:
        template = get_template("analytics.html")
        context = {"code": analytics_id, "domain": domain}
        return template.render(context)
    return ""


@register.filter(name="lookup")
def cut(value, arg):
    return value[arg]


@register.simple_tag
def chosen(oid: str) -> str:
    return mark_safe(
        '<script type="text/javascript">$(document).ready(function(){ $("'
        + oid
        + "\").chosen({ width: '100%' }); });</script>"
    )


@register.filter
def date_is_not_expired(value, arg: Any = None) -> bool:
    """Finds whether the date passed as `value` is later than today."""
    if value:
        return date(value.year, value.month, value.day) >= timezone.now().date()
    return True
