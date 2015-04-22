from django.conf import settings
from django.template import loader
from django.template.base import Library
from django.template.context import Context

register = Library()


@register.simple_tag
def analytics():
    """
    returns the analytics id from the settingsfile, if debug is false
    """
    analytics_id = settings.SITE['analytics']
    domain = settings.SITE['domain']
    if not settings.DEBUG:
        t = loader.get_template('analytics.html')
        c = Context({'code': analytics_id, 'domain': domain})
        return t.render(c)

    else:
        return ""


@register.filter(name='lookup')
def cut(value, arg):
    return value[arg]


@register.simple_tag
def chosen(oid):
    return '<script type="text/javascript">$(document).' \
           'ready(function(){ $("' + oid + '").chosen({ width: \'100%\' }); });</script>'


@register.filter
def date_is_not_expired(value, arg=None):
    """
    Returns True if the date passed as value is later than today
    """
    if value:
        from datetime import date
        return date(value.year, value.month, value.day) >= date.today()
    return True
