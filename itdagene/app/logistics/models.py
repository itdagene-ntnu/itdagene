from django.db import models
from django.utils.translation import ugettext_lazy as _
from itdagene.app.company.models import Company
from itdagene.core.models import BaseModel

class RoomRegistration(BaseModel):
    company = models.ForeignKey(Company, null=True, blank=True, verbose_name=_('company'))
    room_nr = models.CharField(max_length=10, verbose_name=_('room number'))
    date = models.DateField(verbose_name=_('date'))
    time_start = models.TimeField(_('start time'))
    time_end = models.TimeField(verbose_name=_('end time'))
    confirmed = models.BooleanField(verbose_name=_('confirmed'), default=False)
    receipt = models.TextField(blank=True,verbose_name=_('receipt'))


    def __unicode__(self):
        return '%s: %s %s - %s' % (self.company, str(self.date), str(self.time_start), str(self.time_end))