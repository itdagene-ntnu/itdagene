from django.template.base import Library
from django.template import loader
from django.template.context import Context
from django.conf import settings
from itdagene.core.models import Preference

register = Library()

@register.simple_tag
def analytics():

    """
    returns the analytics id from the settingsfile, if debug is false
    """
    analytics_id = settings.SITE['analytics']
    if not settings.DEBUG:
        t = loader.get_template('analytics.html')
        c = Context({'code': analytics_id})
        return t.render(c)

    else:
        return ""


@register.simple_tag
def chosen(oid):
    return '<script type="text/javascript">$(document).ready(function(){ $("' + oid + '").chosen({ width: \'100%\' }); });</script>'

@register.simple_tag
def active_year():
    return Preference.current_preference().year


@register.filter(name='lookup')
def cut(value, arg):
    return value[arg]

@register.filter
def date_is_not_expired(value, arg=None):
    """
    Returns True if the date passed as value is later than today
    """
    if value:
        from datetime import date
        return date(value.year, value.month, value.day) >= date.today()
    return True
