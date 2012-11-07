from django.core.cache import cache
from django.template.base import Library
#from itdagene.core.notifications.models import Notification
register = Library()

@register.simple_tag
def include_tinycon():
    return '<script src="/static/js/tinycon.min.js"></script>'

@register.simple_tag
def set_bubble(size):
    return '<script type="text/javascript">Tinycon.setBubble(%s);</script>' % size

@register.simple_tag
def set_notification_bubble():
    c = cache.get('notificationsforuser%s' % 1)
    if not c: c = 0
    return set_bubble(c)

