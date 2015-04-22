import random
import string
from datetime import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from itdagene.app.company.models import Company
from itdagene.core.auth import generate_password
from itdagene.core.log.models import LogItem
from itdagene.core.models import BaseModel, Preference, User

APPS = (
    ('all', _('All')),
    ('admin',_('Admin')),
    ('company',_('BDB')),
    ('career',_('Career')),
    ('core',_('Core')),
    ('events',_('Events')),
    ('feedback',_('Feedback')),
    ('frontpage',_('Frontpage')),
    ('logistics',_('Logistics')),
    ('mail',_('Mail')),
    ('meetings',_('Meetings')),
    ('news',_('News')),
    ('notifications',_('Notifications')),
    ('pages',_('Pages')),
    ('profiles',_('Profiles')),
    ('todo',_('Todo')),
    ('venue',_('Venue')),
    ('workschedule',_('Workschedule')),
)

TYPES = (
    (0, _('Bug')),
    (1, _('Feature')),
    (2, _('Cache problem')),
)

STATUS = (
    (0, _('New')),
    (1, _('In progress')),
    (2, _('Needs feedback')),
    (3, _('Finished')),
)

class Issue (BaseModel):
    title = models.CharField(max_length=100, verbose_name=_('title'))
    app = models.CharField(max_length=50, choices=APPS,verbose_name=_('app'))
    type = models.PositiveIntegerField(default=1,choices=TYPES, verbose_name=_('type'))
    status = models.PositiveIntegerField(default=0, choices=STATUS, verbose_name=_('status'))
    description = models.TextField(verbose_name=_('description'))
    is_solved = models.BooleanField(verbose_name=_('is solved'), default=False)
    assigned_user = models.ForeignKey(User, related_name='assigned_issues', blank=True, null=True, verbose_name=_('assigned user'))
    deadline = models.DateTimeField(blank=True, null=True, verbose_name=_('deadline'))
    solved_date = models.DateTimeField(blank=True, null=True, verbose_name=_('solved date'))

    def __unicode__(self):
        return self.get_app_display() + ": " + self.title

    def get_absolute_url(self):
        return reverse('itdagene.app.feedback.views.issues.view', args=[self.pk])

    def save(self, *args, **kwargs):
        if self.pk: action = 'EDIT'
        else: action = 'CREATE'
        if self.is_solved and self.solved_date is None:
            self.solved_date = datetime.now()
        super(Issue, self).save(*args, **kwargs)
        LogItem.log_it(self, action,0)

    class Meta:
        verbose_name = _('issue')
        verbose_name_plural = _('issues')


RATINGS = ((0, _('Did not use')), (1,_('1: Very bad')),(2,_('2: Bad')),(3,_('3: Not bad or good')),(4,_('4: Good')),(5, _('5: Very good')))


class Evaluation (models.Model):

    company = models.ForeignKey(Company, verbose_name='Company')
    preference = models.ForeignKey(Preference, verbose_name='Preference')
    hash = models.CharField(max_length=100, verbose_name=_('Hash'), unique=True)
    has_answers = models.BooleanField(default=False, verbose_name=_('has answers'))

    internship_marathon_rating = models.IntegerField(
                        choices=RATINGS,
                        verbose_name=_('How did the kickstart go?'),
                        default=0
                     )
    internship_marathon_improvement = models.TextField(blank=True, verbose_name=_('What could have been done better at the kickstart?'))

    course_rating = models.IntegerField(
                        choices=RATINGS,
                        verbose_name=_('How did the course go?'),
                        default=0
                     )
    course_improvement = models.TextField(blank=True, verbose_name=_('Could the course be handled better?'))

    visitors_rating = models.IntegerField(
        choices=RATINGS,
        verbose_name=_('Are you satisfied with the number of people that visited your stand?'),
        default=0
    )

    has_interview_location = models.BooleanField(verbose_name=_('Did you use interview rooms?'), default=False)
    interview_location_rating = models.IntegerField(
                        choices=RATINGS,
                        verbose_name=_('How was the interview room?'),
                        default=0
                     )
    interview_location_improvement = models.TextField(blank=True, verbose_name=_('What could have been done better?'))




    has_banquet = models.BooleanField(verbose_name=_('Where you at the banquet?'), default=False)
    banquet_rating = models.IntegerField(
        choices=RATINGS,
        verbose_name=_('How did the banquet go?'),
        default=0
    )
    banquet_improvement = models.TextField(blank=True, verbose_name=_('What could have been done better at the banquet?'))


    opening_hours = models.TextField(verbose_name=_('Was the opening hours(10-16) ok? If not what would be your choice?'))
    improvement = models.TextField(verbose_name=_('What could have been done better?'))
    other = models.TextField(blank=True, verbose_name=_('Something else you want to comment?'), help_text=_('Do you have any tips?'))
    want_to_come_back = models.BooleanField(verbose_name=_('Interested in being contacted next year?'), default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.hash = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(50))

        super(Evaluation, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.hash
