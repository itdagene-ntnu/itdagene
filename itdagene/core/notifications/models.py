from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext as _

from itdagene.core.auth import get_current_user
from itdagene.core.models import User


class Notification(models.Model):

    PRIORITIES = ((0, "Low"), (1, "Medium"), (2, "High"))

    priority = models.PositiveIntegerField(
        choices=PRIORITIES, default=1, verbose_name=_("priority")
    )

    date = models.DateTimeField(auto_now=True, verbose_name=_("date"))
    message = models.TextField(verbose_name=_("message"))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    send_mail = models.BooleanField(default=True, verbose_name=_("send mail"))
    sent_mail = models.BooleanField(default=False, verbose_name=_("sent mail"))

    users = models.ManyToManyField(
        User, verbose_name="users", related_name="notifications"
    )

    def __str__(self):
        if len(self.message) > 100:
            return "%s..." % (self.message[0:100],)
        return "%s" % (self.message,)

    def save(self, *args, **kwargs):
        notification = super(Notification, self).save(*args, **kwargs)

        if self.send_mail and not self.sent_mail:
            from itdagene.app.mail.tasks import send_notification_message

            send_notification_message.delay(self)
            self.send_mail = True
            notification = super(Notification, self).save(*args, **kwargs)

        return notification

    def read_notification(self, user):
        raise NotImplementedError()

    @classmethod
    def get_notifications(cls, user):
        return user.notifications.all()

    @classmethod
    def notify(cls, object, users):
        send_mail = bool(object.notification_priority())

        notification = Notification(
            content_object=object,
            priority=object.notification_priority(),
            message=object.notification_message(),
            send_mail=send_mail,
        )

        notification.save()

        for user in users:
            notification.users.add(user)


class Subscription(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    subscribers = models.ManyToManyField(User, blank=True, related_name="subscriptions")

    class Meta:
        unique_together = ("content_type", "object_id")

    @classmethod
    def notify_subscribers(cls, object):
        notification_object_ct = ContentType.objects.get_for_model(
            object.notification_object()
        )

        try:
            subscription = Subscription.objects.get(
                content_type=notification_object_ct,
                object_id=object.notification_object().id,
            )

            subscribers = subscription.subscribers.all()

            current_user = get_current_user()
            if current_user:
                subscribers = subscribers.exclude(id=current_user.id)

            Notification.notify(object, subscribers.distinct("pk"))

        except cls.DoesNotExist:
            return

    @classmethod
    def subscribe(cls, object, user):
        subscription = Subscription.get_or_create(object)
        if user and not user.is_anonymous:
            if user not in list(subscription.subscribers.all()):
                subscription.subscribers.add(user)
        subscription.save()

    @classmethod
    def get_or_create(cls, object):
        content_type = ContentType.objects.get_for_model(object)
        try:
            subscription = Subscription.objects.get(
                content_type=content_type, object_id=object.id
            )
        except (TypeError, Subscription.DoesNotExist):
            subscription = Subscription(content_type=content_type, object_id=object.id)
            subscription.save()
        return subscription
