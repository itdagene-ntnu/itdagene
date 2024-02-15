from typing import Dict

from django.http import HttpRequest
from django.template import Library

from itdagene.core.notifications.models import Notification

register = Library()


@register.inclusion_tag("core/notifications/list.html")
def notification_list(request: HttpRequest) -> Dict[str, Notification]:
    """Gets the notification list."""
    notifications = Notification.get_notifications(user=request.user)
    return {"notifications": notifications}
