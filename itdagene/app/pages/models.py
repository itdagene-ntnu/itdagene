from django.conf import settings
from django.db.models import BooleanField, CharField, FileField, SlugField, TextField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from itdagene.core.log.models import LogItem
from itdagene.core.models import BaseModel


class Page(BaseModel):
    title = CharField(max_length=100, verbose_name=_("title"))
    slug = SlugField(max_length=100, verbose_name=_("slug"))
    content = TextField(verbose_name=_("content"))
    ingress = TextField(verbose_name=_("ingress"), default="")
    language = CharField(
        max_length=3,
        default=settings.DEFAULT_LANGUAGE,
        choices=settings.LANGUAGES,
    )
    active = BooleanField(verbose_name=_("active"), default=False)
    need_auth = BooleanField(verbose_name=_("need authentication"), default=False)
    menu = BooleanField(verbose_name=_("should be in menu"), default=False)
    is_infopage = BooleanField(verbose_name=_("is an info page"), default=False)

    video_file = FileField(upload_to="pageVideos/", null=True, blank=True)

    def __str__(self) -> str:
        return str(self.title)

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    def save(self, *args, **kwargs) -> None:
        action = "EDIT" if self.pk else "CREATE"
        super(Page, self).save(*args, **kwargs)
        LogItem.log_it(self, action, 1)
        self.last_saved = timezone.now()
