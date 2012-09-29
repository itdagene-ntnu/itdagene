from itdagene.app.company.models import Company
from itdagene.core.models import BaseModel
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class Milestone (BaseModel):
    title = models.CharField(max_length=80, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'))
    deadline = models.DateTimeField(verbose_name=_('deadline'))
    todo_per_company = models.BooleanField(verbose_name=_('todo for each company'),
                                           help_text=_('If unchecked there will only be created a todo for each board-user'))

    def __unicode__(self):
        return self.title


class Todo (BaseModel):
    title = models.CharField(max_length=80, verbose_name=_('title'))
    user = models.ForeignKey(User, related_name='todos', verbose_name=_('user'))
    company = models.ForeignKey(Company, blank=True, null=True, related_name='todos', verbose_name=_('company'))
    milestone = models.ForeignKey(Milestone, blank=True, null=True, related_name='todos', verbose_name=_('milestone'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    deadline = models.DateTimeField(blank=True, null=True, verbose_name=_('deadline'))
    finished = models.BooleanField(verbose_name=_('finished'))

    def __unicode__(self):
        return self.title