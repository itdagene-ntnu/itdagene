from typing import Any

from django.conf import settings
from django.template import Library
from django.utils import dateformat
from django.utils.formats import date_format
from django.utils.safestring import mark_safe
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _


register = Library()


@register.filter
def boolean(value: Any, arg: Any = None) -> str:
    """Finds HTML markup for a Glyphicon based on the truthiness of the
    `value`.
    """
    if value:
        return mark_safe('<span class="glyphicon glyphicon-ok" alt="yes">')
    return mark_safe('<span class="glyphicon glyphicon-remove" alt="no">')


@register.filter
def has_contract_for_current_year(value: list, arg=None) -> bool:
    """Decides whether the contract passed as `value` is from current
    year.
    """
    # ? Why is arg=None? Return False if arg is None?
    return any(contract.timestamp.year == int(arg) for contract in value)


@register.filter
def datetime(value, arg: Any = None) -> str:
    """Find a date with timeleft and the datetime format from the
    settingsfile. A js will animate between the two types on mouseover.
    """
    time_since = ""
    normal = ""
    if not value:
        return ""

    try:
        time_since = timesince(value)
    except (ValueError, TypeError):
        return ""

    try:
        normal = date_format(value, settings.DATETIME_FORMAT)
    except AttributeError:
        try:
            normal = dateformat.format(value, settings.DATETIME_FORMAT)
        except AttributeError:
            return ""

    return mark_safe(
        f'<span class="date"><span class="date-ts"> for {time_since} '
        f'{_("ago")}</span><span class="date-normal" style="display:none;">'
        f"{normal}</span></span>"
    )
