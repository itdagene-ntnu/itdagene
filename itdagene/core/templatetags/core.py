from django.template.base import Library
from django.template import loader
from django.template.context import Context
from django.conf import settings

register = Library()

@register.simple_tag
def analytics():

    """
    returns the analytics id from the settingsfile, if debug is false
    """
    analytics_id = settings.ANALYTICS
    if not settings.DEBUG:
        t = loader.get_template ('analytics.html')
        c = Context({'code': analytics_id})
        return t.render(c)

    else:
        return ""


@register.simple_tag
def chosen(oid):
    return '<script type="text/javascript">$(document).ready(function(){ $("#%s").chosen(); });</script>' % oid