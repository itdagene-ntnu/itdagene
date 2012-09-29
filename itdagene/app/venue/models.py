from django.db import models
from itdagene.app.company.models import Company
from itdagene.core.log.models import LogItem
from itdagene.core.models import BaseModel

class Stand(BaseModel):
    section = models.CharField(max_length=1)
    stand_nr = models.PositiveIntegerField()
    company_day1 = models.ForeignKey(Company, related_name='stand_day1', null=True, blank=True)
    company_day2 = models.ForeignKey(Company, related_name='stand_day2', null=True, blank=True)

    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    lon = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)

    def __unicode__(self):
        return self.section + str(self.stand_nr)

    def save(self, *args, **kwargs):
        self.section = self.section.upper()
        if self.pk: action = 'EDIT'
        else: action = 'CREATE'
        super(Stand, self).save(*args, **kwargs)
        LogItem.log_it(self, action, 1)