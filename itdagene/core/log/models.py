from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from itdagene.app.mail.tasks import send_admin_mail
from itdagene.core.auth import get_current_user
from itdagene.core.models import User


class LogItem(models.Model):

    PRIORITIES = (
        (0, "Low"),
        (1, "Medium"),
        (2, "High"),
        (3, "Very High. Will send email to administrators"),
    )

    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    priority = models.PositiveIntegerField(
        choices=PRIORITIES, default=1, verbose_name=_("priority")
    )
    timestamp = models.DateTimeField(auto_now=True, verbose_name=_("date"))
    action = models.CharField(max_length=16, verbose_name=_("action"))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.action

    def save(self, *args, **kwargs):
        if self.priority == 3:
            send_admin_mail.delay(self)
        super(LogItem, self).save(*args, **kwargs)

    @classmethod
    def log_it(cls, object, action, priority):
        user = get_current_user()
        if not user or not user.is_authenticated:
            user = User.objects.first()
        log_item = LogItem(
            user=user,
            priority=priority,
            timestamp=timezone.now(),
            action=action,
            object_id=object.pk,
            content_type=ContentType.objects.get_for_model(object),
        )
        log_item.save()
