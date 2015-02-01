from django.core.urlresolvers import reverse
from itdagene.core.notifications.models import Notification


class NotificationsMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            path = request.path
            notifications = Notification.objects.filter(user=request.user, read=False).select_related('content_object')
            if notifications:
                for notification in notifications:
                    if notification.content_object.get_absolute_url() == path:
                        notification.read_notification()
