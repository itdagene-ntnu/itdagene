from django.db import models
from itdagene.core.models import BaseModel
from django.utils.translation import ugettext_lazy as _


class Document (BaseModel):
    file = models.FileField(upload_to='documents/', verbose_name=_('file'))

    def __unicode__(self):
        return u'%s' % self.file.name
