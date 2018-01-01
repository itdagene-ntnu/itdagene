from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from itdagene.core.models import BaseModel, User


class Todo(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='todos',
        verbose_name=_('user'),
    )
    description = models.TextField(verbose_name=_('description'))
    deadline = models.DateTimeField(blank=True, null=True, verbose_name=_('deadline'))
    finished = models.BooleanField(verbose_name=_('finished'), default=False)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('itdagene.todo.view_todo', args=[self.pk])
