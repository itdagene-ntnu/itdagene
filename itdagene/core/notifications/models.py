from typing import Any

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import (
    CASCADE,
    BooleanField,
    DateTimeField,
    ForeignKey,
    ManyToManyField,
    Model,
    PositiveIntegerField,
    TextField,
)
from django.utils.translation import gettext_lazy as _

from itdagene.core.auth import get_current_user
from itdagene.core.models import BaseModel, User


class Notification(Model):
    PRIORITIES = ((0, "Low"), (1, "Medium"), (2, "High"))

    priority = PositiveIntegerField(
        choices=PRIORITIES, default=1, verbose_name=_("priority")
    )

    date = DateTimeField(auto_now=True, verbose_name=_("date"))
    message = TextField(verbose_name=_("message"))
    content_type = ForeignKey(ContentType, on_delete=CASCADE)
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    send_mail = BooleanField(default=True, verbose_name=_("send mail"))
    sent_mail = BooleanField(default=False, verbose_name=_("sent mail"))

    users = ManyToManyField(User, verbose_name="users", related_name="notifications")

    def __str__(self) -> str:
        max_length = 100
        if len(self.message) > max_length:
            return f"{self.message[:max_length]}..."
        return self.message

    def save(self, *args, **kwargs) -> None:
        notification = super(Notification, self).save(*args, **kwargs)

        if self.send_mail and not self.sent_mail:
            from itdagene.app.mail.tasks import send_notification_message

            send_notification_message.delay(self)
            self.send_mail = True
            notification = super(Notification, self).save(
                *args, **kwargs
            )  # ? Always None

        return notification

    def read_notification(self, user: Any) -> None:
        raise NotImplementedError()

    @classmethod
    def get_notifications(cls, user):
        return user.notifications.all()

    @classmethod
    def notify(cls, object: Any, users) -> None:
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


class Subscription(Model):
    content_type = ForeignKey(ContentType, on_delete=CASCADE)
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey()
    subscribers = ManyToManyField(User, blank=True, related_name="subscriptions")

    class Meta:
        unique_together = ("content_type", "object_id")

    @classmethod
    def notify_subscribers(cls, object: BaseModel) -> None:
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
    def subscribe(cls, object_: Model, user) -> None:
        subscription = Subscription.get_or_create(object_)
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
