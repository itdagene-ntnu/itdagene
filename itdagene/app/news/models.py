from django.utils.translation import ugettext_lazy as _
from itdagene.core.models import BaseModel
from django.db import models


class Announcement (BaseModel):
    title = models.CharField(max_length=100, verbose_name=_('title'))
    content = models.TextField(verbose_name=_('content'))
    image = models.ImageField(upload_to='announcements/',verbose_name=_('image'))

    class Meta:
        verbose_name = _('announcement')
        verbose_name_plural = _('announcements')

    def __unicode__(self):
        return self.title
