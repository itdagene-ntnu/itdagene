from django.db.models import BooleanField, CharField, ImageField, TextField
from django.utils.translation import gettext_lazy as _

from itdagene.core.models import BaseModel


class Announcement(BaseModel):
    title = CharField(max_length=100, verbose_name=_("title"))
    content = TextField(verbose_name=_("content"))
    image = ImageField(blank=True, upload_to="announcements/", verbose_name=_("image"))
    public = BooleanField(default=False, verbose_name=_("public"))

    class Meta:
        verbose_name = _("announcement")
        verbose_name_plural = _("announcements")

    def __str__(self) -> str:
        return str(self.title)
