from django.utils import timezone

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from itdagene.core.log.models import LogItem
from itdagene.core.models import BaseModel


class Page(BaseModel):
    title = models.CharField(max_length=100, verbose_name=_('title'))
    slug = models.SlugField(max_length=100, verbose_name=_('slug'))
    content = models.TextField(verbose_name=_('content'))
    language = models.CharField(
        max_length=3, default=settings.DEFAULT_LANGUAGE, choices=settings.LANGUAGES
    )
    active = models.BooleanField(verbose_name=_('active'), default=False)
    need_auth = models.BooleanField(verbose_name=_('need authentication'), default=False)
    menu = models.BooleanField(verbose_name=_('should be in menu'), default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')

    def save(self, *args, **kwargs):
        action = 'EDIT' if self.pk else 'CREATE'
        super(Page, self).save(*args, **kwargs)
        LogItem.log_it(self, action, 1)
        self.last_saved = timezone.now()
