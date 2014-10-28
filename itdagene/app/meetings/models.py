from django.conf import settings
from django.db import models
from itdagene.core.log.models import LogItem
from itdagene.core.models import BaseModel
from itdagene.core.models import User, Preference
from django.utils.translation import ugettext_lazy as _, ugettext
from django.core.urlresolvers import reverse

MEETING_TYPES = (
    (0, _('Board meeting')),
    (1, _('Web')),
    (2, _('Banquet')),
    (3, _('Logistics')),
    (4, _('Marketing')),
    (5, _('Other')),
)

class Meeting(BaseModel):
    date = models.DateField(verbose_name=_('date'))
    start_time = models.TimeField(verbose_name=_('from time'))
    end_time = models.TimeField(blank=True, null=True, verbose_name=_('to time'))
    type = models.PositiveIntegerField(choices=MEETING_TYPES, default=0, verbose_name=_('type'))
    location = models.CharField(max_length=40,blank=True, verbose_name=_('location'))
    agenda = models.TextField(blank=True, null=True, verbose_name=_('Meeting Agenda'))
    abstract = models.TextField(blank=True, null=True, verbose_name=_('abstract'))
    is_board_meeting = models.BooleanField(default=True, verbose_name=_('is board meeting'))
    referee = models.ForeignKey(User, related_name='refereed_meetings', null=True, blank=True, verbose_name=_('referee'))
    preference = models.ForeignKey(Preference, verbose_name='Preference', blank=True, null=True)

    def __unicode__(self):
        return self.get_type_display()

    def save(self, *args, **kwargs):
        super(Meeting, self).save(*args, **kwargs)

    def attending(self):
        att = list(self.replies.filter(is_attending=True))
        return att

    def not_attending(self):
        att = list(self.replies.filter(is_attending=False))
        return att

    def awaiting_reply(self):
        att = list(self.replies.filter(is_attending=None))
        return att

    def attending_link(self):
        return 'http://%s%s' % (settings.SITE['domain'], reverse('itdagene.app.meetings.views.attend', args=[self.pk]))

    def not_attending_link(self):
        return 'http://%s%s' % (settings.SITE['domain'], reverse('itdagene.app.meetings.views.not_attend', args=[self.pk]))

    def get_absolute_url(self):
        return reverse('itdagene.app.meetings.views.meeting', args=(self.pk,))

    class Meta:
        verbose_name = _('meeting')
        verbose_name_plural = _('meetings')


class ReplyMeeting(BaseModel):
    meeting = models.ForeignKey(Meeting, related_name='replies',verbose_name=_('meeting'))
    user = models.ForeignKey(User, verbose_name=_('user'))
    is_attending = models.NullBooleanField(verbose_name=_('attending'), null=True, blank=True)
    
    def __unicode__(self):
        return ugettext('Meeting participation: %s' % self.user)

    def get_absolute_url(self):
        return reverse('itdagene.app.meetings.views.meeting', args=(self.meeting.pk,))

    def save(self, *args, **kwargs):
        super(ReplyMeeting, self).save()


class Penalty(BaseModel):
    TYPES = (
        ('beer', _('Beer')),
        ('wine', _('Wine')),
    )
    user = models.ForeignKey(User, related_name='penalties', verbose_name=_('person'))
    meeting = models.ForeignKey(Meeting, blank=True, null=True, verbose_name=_('meeting'))
    type = models.CharField(max_length=10, default='beer', choices=TYPES, verbose_name=_('type'))
    bottles = models.PositiveIntegerField(default=2, verbose_name=_('number of bottles'))
    reason = models.TextField(verbose_name=_('reason'))

    def __unicode__(self):
        return self.user.username + ' ' + str(self.bottles) + ' ' + self.get_type_display()

    def save(self, *args, **kwargs):
        if self.pk: action = 'EDIT'
        else: action = 'CREATE'
        super(Penalty, self).save(*args, **kwargs)
        LogItem.log_it(self, action, 1)
