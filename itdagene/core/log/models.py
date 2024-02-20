from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    PositiveIntegerField,
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from itdagene.app.mail.tasks import send_admin_mail
from itdagene.core.auth import get_current_user
from itdagene.core.models import User


class LogItem(Model):
    PRIORITIES = (
        (0, "Low"),
        (1, "Medium"),
        (2, "High"),
        (3, "Very High. Will send email to administrators"),
    )

    user = ForeignKey(User, verbose_name=_("user"), on_delete=CASCADE)
    priority = PositiveIntegerField(
        choices=PRIORITIES, default=1, verbose_name=_("priority")
    )
    timestamp = DateTimeField(auto_now=True, verbose_name=_("date"))
    action = CharField(max_length=16, verbose_name=_("action"))
    content_type = ForeignKey(ContentType, on_delete=CASCADE)
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self) -> str:
        return self.action

    def save(self, *args, **kwargs) -> None:
        if self.priority == 3:
            send_admin_mail.delay(self)
        super(LogItem, self).save(*args, **kwargs)

    @classmethod
    def log_it(cls, object_: Model, action: str, priority: int) -> None:
        user = get_current_user()
        if not user or not user.is_authenticated:
            user = User.objects.first()
        log_item = LogItem(
            user=user,
            priority=priority,
            timestamp=timezone.now(),
            action=action,
            object_id=object_.pk,
            content_type=ContentType.objects.get_for_model(object_),
        )
        log_item.save()
