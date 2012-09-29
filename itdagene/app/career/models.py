from datetime import date
from django.utils.translation import ugettext_lazy as _
from itdagene.app.company.models import Company, CompanyContact
from itdagene.core.models import BaseModel
from django.db import models
from django.core.urlresolvers import reverse

class Town (BaseModel):
    name = models.CharField(max_length=100, verbose_name=_('name'))

    def __unicode__(self):
        return self.name

class Joblisting (BaseModel):

    JOB_TYPES = (
        ('si',_('Summer internship')),
        ('pp',_('Permanent position')),
        ('bi',_('Bad import')),
    )

    company = models.ForeignKey(Company, related_name='joblistings', verbose_name=_('company'))
    title = models.CharField(max_length=160, verbose_name=_('title'))
    type = models.CharField(max_length=20, choices=JOB_TYPES, verbose_name=_('type'))
    description = models.TextField()
    contact = models.ForeignKey(CompanyContact,null=True,blank=True, verbose_name=_('contact'))
    image = models.ImageField(upload_to='joblistings/', null=True, blank=True, verbose_name=_('image'))
    deadline = models.DateField(null=True, blank=True, verbose_name=_('deadline'))
    from_year = models.PositiveIntegerField(default=1)
    to_year = models.PositiveIntegerField(default=5)
    towns = models.ManyToManyField(Town, null=True, blank=True, verbose_name=_('town'))
    url = models.URLField(blank=True, verbose_name=_('url'))


    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('app.career.views.joblistings.view_joblistings', args=[self.pk])

    def has_deadline_passed(self):
        return self.deadline < date.today()