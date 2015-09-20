from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from itdagene.app.company.models import Company
from itdagene.core.models import BaseModel

EVENT_TYPES = (
    (0, _('Course')),
    (1, _('Company presentation')),
    (2, _('Banquet')),
    (3, _('Summer internship marathon')),
    (4, _('Baloon drop'))
)


class Event(BaseModel):
    title = models.CharField(max_length=80, verbose_name=_('title'))
    date = models.DateField(verbose_name=_('date'))
    time_start = models.TimeField(verbose_name=_('start time'))
    time_end = models.TimeField(verbose_name=_('end time'))
    description = models.TextField(verbose_name=_('description'))
    type = models.PositiveIntegerField(choices=EVENT_TYPES,
                                       verbose_name=_('type'))
    location = models.CharField(max_length=30, verbose_name=_('location'))
    is_internal = models.BooleanField(verbose_name=_('internal event'),
                                      default=False)
    company = models.ForeignKey(Company,
                                null=True,
                                blank=True,
                                verbose_name=_('hosting company'))
    uses_tickets = models.BooleanField(verbose_name=_('uses tickets'),
                                       default=False)
    max_participants = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('max nr of participants'))

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('itdagene.app.events.views.view_event', args=[self.pk])


class Ticket(BaseModel):
    event = models.ForeignKey(Event,
                              related_name='tickets',
                              verbose_name=_('event'))
    company = models.ForeignKey(Company,
                                related_name='tickets',
                                null=True,
                                blank=True,
                                verbose_name=_('company'))
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('e-mail address'), blank=True)

    class Meta:
        ordering = ('last_name', )

    def __unicode__(self):
        return '%s: %s' % (self.event.title, self.full_name())

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)
