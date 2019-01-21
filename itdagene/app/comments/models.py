from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from itdagene.core.models import User


class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    comment = models.TextField(verbose_name=_("comment"))
    date = models.DateTimeField(verbose_name=_("date"))
    object = GenericForeignKey("content_type", "object_id")
    object_id = models.PositiveIntegerField(null=True)
    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.SET_NULL)
    reply_to = models.ForeignKey(
        "self", related_name="replies", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return str(self.user)
