from django.db import models
from itdagene.app.company.models import Company
from itdagene.core.models import BaseModel, Preference
from django.utils.translation import ugettext_lazy as _


class Stand(BaseModel):
    section = models.CharField(max_length=1)
    stand_nr = models.PositiveIntegerField()

    def __unicode__(self):
        return self.section + str(self.stand_nr)

    def save(self, *args, **kwargs):
        self.section = self.section.upper()
        super(Stand, self).save(*args, **kwargs)


class StandCompany(BaseModel):
    stand = models.ForeignKey(Stand, verbose_name=_('stand'), related_name='stand_companies')
    date = models.DateField(verbose_name=_('date'))
    company = models.ForeignKey(Company, verbose_name=_('company'), related_name='stands')

    class Meta:
        unique_together = (('date', 'stand'), ('date', 'company'))
