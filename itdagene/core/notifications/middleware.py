from django.utils.deprecation import MiddlewareMixin


class NotificationsMiddleware(MiddlewareMixin):
    """This middleware is used to remove notifications automatically.
    This was a performance issue. It disabled. This needs caching to
    work.
    """

    def process_request(self, request):
        user = getattr(request, "user", None)
        if user and user.is_authenticated:
            path = request.path
            notifications = request.user.notifications.prefetch_related(
                "content_object"
            ).all()

            for notification in notifications:
                if not notification.content_object:
                    notification.delete()
                    continue
                if notification.content_object.get_absolute_url() == path:
                    notification.users.remove(user)
                    if notification.users.count == 0:
                        notification.delete()

        return self.get_response(request)
