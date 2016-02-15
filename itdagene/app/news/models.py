from django.db import models
from django.utils.translation import ugettext_lazy as _

from itdagene.core.models import BaseModel


class Announcement(BaseModel):
    title = models.CharField(max_length=100, verbose_name=_('title'))
    content = models.TextField(verbose_name=_('content'))
    image = models.ImageField(blank=True, upload_to='announcements/',
                              verbose_name=_('image'))
    public = models.BooleanField(default=False, verbose_name=_('public'))

    class Meta:
        verbose_name = _('announcement')
        verbose_name_plural = _('announcements')

    def __unicode__(self):
        return self.title
