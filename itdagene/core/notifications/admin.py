from django.contrib import admin

from itdagene.core.notifications.models import Notification, Subscription


admin.site.register(Notification)
admin.site.register(Subscription)
