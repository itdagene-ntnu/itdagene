from django.core import cache
from django.template.base import Library
from itdagene.core.notifications.models import Notification

register = Library()

@register.inclusion_tag('core/notifications/list.html')
def notification_list(request):

    """
    returns the notificationlist
    """
    notifications = Notification.objects.filter(user=request.user).order_by('date')
    return {'notifications': notifications}