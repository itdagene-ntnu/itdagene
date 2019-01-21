from django.template import Library
from django.utils import formats
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

register = Library()


@register.filter
def boolean(value, arg=None):
    """
    Returns HTML markup for a Glyphicon based on the truthiness of the value
    """
    if value:
        return mark_safe('<span class="glyphicon glyphicon-ok" alt="yes">')
    return mark_safe('<span class="glyphicon glyphicon-remove" alt="no">')


@register.filter
def has_contract_for_current_year(value, arg=None):
    """
    Returns True if the contract passed as value is from current year
    """
    for contract in value:
        if contract.timestamp.year == int(arg):
            return True
    return False


@register.filter
def datetime(value, arg=None):
    """
    returns a date with timeleft and the datetime format from the settingsfile. A js will animate
    between the two types on mouseover.
    """
    from django.utils.timesince import timesince
    from django.utils.dateformat import format
    from django.conf import settings

    ts = ""
    normal = ""
    if not value:
        return ""
    try:
        ts = timesince(value)
    except (ValueError, TypeError):
        return ""
    try:
        normal = formats.date_format(value, settings.DATETIME_FORMAT)
    except AttributeError:
        try:
            normal = format(value, settings.DATETIME_FORMAT)
        except AttributeError:
            return ""
    return mark_safe(
        '<span class="date"><span class="date-ts"> for %s %s</span><span class="date-normal" '
        'style="display:none;">%s</span></span>' % (ts, _("ago"), normal)
    )
