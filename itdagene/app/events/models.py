from datetime import datetime
from django.db import models
from itdagene.app.company.models import Company
from itdagene.core.models import BaseModel
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django import forms

EVENT_TYPES = (
    (0, _('Course')),
    (1, _('Company presentation')),
    (2, _('Banquet')),
)

class Event(BaseModel):
    title = models.CharField(max_length=80, verbose_name=_('title'))
    date = models.DateField(verbose_name=_('date'))
    time_start = models.TimeField(verbose_name=_('start time'))
    time_end = models.TimeField(verbose_name=_('end time'))
    description = models.TextField(verbose_name=_('description'))
    type = models.PositiveIntegerField(choices=EVENT_TYPES, verbose_name=_('type'))
    location = models.CharField(max_length=30, verbose_name=_('location'))
    is_internal = models.BooleanField(verbose_name=_('internal event'))
    company = models.ForeignKey(Company, null=True, blank=True,verbose_name=_('hosting company'))
    uses_tickets = models.BooleanField(verbose_name=_('uses tickets'))
    max_participants = models.PositiveIntegerField(null=True, blank=True,verbose_name=_('max nr of participants'))

    def __unicode__(self):
        return self.title




class Ticket(BaseModel):
    event = models.ForeignKey(Event, related_name='tickets', verbose_name=_('event'))
    company = models.ForeignKey(Company, related_name='tickets', null=True, blank=True,verbose_name=_('company'))
    user = models.ForeignKey(User, null=True, blank=True, verbose_name=_('user'), help_text=_('If the person does not have a user, use the fields below.'))
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('e-mail address'), blank=True)

    class Meta:
        ordering = ('company__name'),

    def __unicode__(self):
        return '%s: %s' % (self.event.title, self.full_name())

    def full_name(self):
        if self.user: return self.user.profile
        else: return '%s %s' % (self.first_name, self.last_name)



    @classmethod
    def extra_tickets_used(cls, event):
        companies = [ticket.company for ticket in cls.objects.filter(event=event)]
        checked_companies = {}
        out = 0
        for company in companies:
            if company in checked_companies:
                continue
            checked_companies[company] = True
            if not company.mp and ((company.partner and Ticket.objects.filter(event=event, company=company).count() > 3) or (not company.partner and Ticket.objects.filter(event=event, company=company).count() > 1)):
                out += 1
        return out
