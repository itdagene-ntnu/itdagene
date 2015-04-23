
class NotificationsMiddleware(object):
    """
    This middleware is used to remove notifications automatically. This was a performance issue.
    It disabled. This needs caching to work.
    """

    def process_request(self, request):

        user = getattr(request, 'user', None)
        if user and user.is_authenticated():

            path = request.path
            notifications = request.user.notifications.select_related('content_object').all()

            for notification in notifications:
                if notification.content_object.get_absolute_url() == path:
                    notification.users.remove(user)
                    if notification.users.count == 0:
                        notification.delete()
