from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import (
    CASCADE,
    SET_NULL,
    DateTimeField,
    ForeignKey,
    Model,
    PositiveIntegerField,
    TextField,
)
from django.utils.translation import gettext_lazy as _

from itdagene.core.models import User


class Comment(Model):
    user = ForeignKey(User, verbose_name=_("user"), on_delete=CASCADE)
    comment = TextField(verbose_name=_("comment"))
    date = DateTimeField(verbose_name=_("date"))
    object = GenericForeignKey("content_type", "object_id")
    object_id = PositiveIntegerField(null=True)
    content_type = ForeignKey(ContentType, null=True, on_delete=SET_NULL)
    reply_to = ForeignKey(
        "self",
        related_name="replies",
        on_delete=SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return str(self.user)
