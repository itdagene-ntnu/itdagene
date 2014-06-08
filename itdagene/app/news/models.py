from django.utils.translation import ugettext_lazy as _
from itdagene.core.models import BaseModel
from django.db import models
from itdagene.core.util.cache import expire_page_cache

class Announcement (BaseModel):
    title = models.CharField(max_length=100, verbose_name=_('title'))
    content = models.TextField(verbose_name=_('content'))
    image = models.ImageField(upload_to='announcements/',verbose_name=_('image'))

    class Meta:
        verbose_name=_('announcement')
        verbose_name_plural=_('announcements')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Announcement, self).save(args, kwargs)
        expire_page_cache('frontpage')
        expire_page_cache('view_announcement', args=[self.pk])