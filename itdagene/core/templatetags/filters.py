from django.template.base import Library
from django.utils import formats
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

register = Library()

@register.filter
def datetime(value, arg=None):
    """
    returns a date with timeleft and the datetime format from the settingsfile. A js will animate between the two types on mouseover.
    """
    from django.utils.timesince import timesince
    from django.utils.dateformat import format
    from django.conf import settings
    ts = ""
    normal = ""
    if not value:
        return u''
    try:
        ts = timesince(value)
    except (ValueError, TypeError):
        return u''
    try:
        normal = formats.date_format(value, settings.DATETIME_FORMAT)
    except AttributeError:
        try:
            normal = format(value, settings.DATETIME_FORMAT)
        except AttributeError:
            return ''
    return mark_safe('<span class="date"><span class="date-ts">%s %s</span><span class="date-normal">%s</span></span>'
                     % (ts, _('ago'), normal))


@register.filter
def boolean(value, arg=None):
    """
    Returns HTML markup for a Glyphicon based on the truthiness of the value
    """
    if value: return mark_safe('<span class="glyphicon glyphicon-ok" alt="%s"' % _('Yes'))
    return mark_safe('<span class="glyphicon glyphicon-remove" alt="%s"' % _('No'))


@register.filter
def has_contract_for_current_year(value, arg=None):
    """
    Returns True if the contract passed as value is from current year
    """
    from datetime import datetime
    for contract in value:
        if contract.timestamp.year == datetime.now().year:
            return True
    return False

@register.filter
def date_is_not_expired(value, arg=None):
    """
    Returns True if the date passed as value is later than today
    """
    if value:
        from datetime import date
        return date(value.year, value.month, value.day) >= date.today()
    return True