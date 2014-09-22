from django.conf import settings
from django.core.cache import cache
from django.db import models
from itdagene.core.log.models import LogItem
from itdagene.core.models import BaseModel
from itdagene.core.models import User
from django.utils.translation import ugettext_lazy as _
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
    abstract = models.TextField(blank=True, null=True, verbose_name=_('abstract'))
    is_board_meeting = models.BooleanField(default=True, verbose_name=_('is board meeting'))
    referee = models.ForeignKey(User, related_name='refereed_meetings', null=True, blank=True, verbose_name=_('referee'))

    def __unicode__(self):
        return str(self.date) + ' ' + str(self.start_time)

    def save(self, *args, **kwargs):
        if not self.pk:
            action = 'CREATE'
        else: action = 'EDIT'
        super(Meeting, self).save(*args, **kwargs)
        LogItem.log_it(self, action, 1)

    def attending(self):
        att = cache.get('meetingsattending' + str(self.id))
        if not att:
            att = list(self.replies.filter(is_attending=True))
            cache.set('meetingsattending' + str(self.id), att)
        return att

    def not_attending(self):
        att = cache.get('meetingsnotattending' + str(self.id))
        if not att:
            att = list(self.replies.filter(is_attending=False))
            cache.set('meetingsnotattending' + str(self.id), att)
        return att

    def awaiting_reply(self):
        att = cache.get('meetingsawaiting' + str(self.id))
        if not att:
            att = list(self.replies.filter(is_attending=None))
            cache.set('meetingsawaiting' + str(self.id), att)
        return att

    def attending_link(self):
        return 'http://%s/meetings/%s/' % (settings.SITE_URL, str(self.pk))

    def not_attending_link(self):
        return 'http://%s/meetings/%s/not-attend' % (settings.SITE_URL, str(self.pk))

    def get_absolute_url(self):
        return reverse('itdagene.app.meetings.views.meeting', args=(self.pk,))

    class Meta:
        verbose_name = _('meeting')
        verbose_name_plural = _('meetings')



class ReplyMeeting(BaseModel):
    meeting = models.ForeignKey(Meeting, related_name='replies',verbose_name=_('meeting'))
    user = models.ForeignKey(User, verbose_name=_('user'))
    is_attending = models.NullBooleanField(verbose_name=_('attending'), default=False)
    
    def __unicode__(self):
        return unicode(self.meeting) + ': ' + self.user.username

    def save(self, *args, **kwargs):
        if self.pk: action = 'EDIT'
        else: action = 'CREATE'
        super(ReplyMeeting, self).save()
        LogItem.log_it(self, action, 1)
        cache.delete('meetingsatteding' + str(self.meeting_id))
        cache.delete('meetingsnotatteding' + str(self.meeting_id))
        cache.delete('meetingsawaiting' + str(self.meeting_id))


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
        cache.delete('totalpenalties' + self.type)
