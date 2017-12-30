from django.db import models
from django.utils.translation import ugettext_lazy as _

from itdagene.core.log.models import LogItem
from itdagene.core.models import BaseModel


class Worker(BaseModel):
    SIZES = (
        (1, 'XS'),
        (2, 'S'),
        (3, 'M'),
        (4, 'L'),
        (5, 'XL'),
        (6, 'XXL'),
        (7, 'XXXL'),
        (8, 'XXXXL'),
    )

    name = models.CharField(max_length=100, verbose_name=_('name'))
    phone = models.IntegerField(verbose_name=_('phone number'), default=0)
    t_shirt_size = models.IntegerField(choices=SIZES, verbose_name=_('t-shirt size'), default=0)
    email = models.EmailField(verbose_name=_('email'), blank=True)
    preference = models.PositiveIntegerField(verbose_name=_('year'))

    def __str__(self):
        return self.name

    def schedules(self):
        return [
            i.schedule
            for i in self.in_schedules.all().order_by('schedule__date', 'schedule__start_time')
        ]

    def as_dict(self):
        return {
            'name': str(self.name),
            'phone': self.phone,
            't_shirt_size': self.t_shirt_size,
            'email': self.email,
        }

    class Meta:
        permissions = (("view_worker", "Can see worker"), )


class WorkSchedule(BaseModel):
    title = models.CharField(max_length=80, verbose_name=_('title'))
    date = models.DateField(verbose_name=_('date'))
    start_time = models.TimeField(verbose_name=_('start time'))
    end_time = models.TimeField(verbose_name=_('end time'))
    description = models.TextField(blank=True, verbose_name=_('Description'))

    def __str__(self):
        return self.title

    def workers(self):
        return [w.worker for w in self.workers_in_schedule.all()]

    def save(self, *args, **kwargs):
        if self.pk:
            action = 'EDIT'
        else:
            action = 'CREATE'
        super(WorkSchedule, self).save(*args, **kwargs)
        LogItem.log_it(self, action, 1)

    def as_dict(self):
        return {
            'title': self.title,
            'date': str(self.date),
            'start_time': str(self.start_time),
            'end_time': str(self.end_time),
            'description': self.description,
        }

    class Meta:
        verbose_name = _('work schedule')
        verbose_name_plural = _('work schedules')
        permissions = (("view_workschedule", "Can see workschedule"), )


class WorkerInSchedule(BaseModel):
    schedule = models.ForeignKey(
        WorkSchedule, on_delete=models.CASCADE, related_name='workers_in_schedule',
        verbose_name=_('schedule')
    )
    worker = models.ForeignKey(
        Worker, on_delete=models.CASCADE, related_name='in_schedules', verbose_name=_('worker')
    )
    has_met = models.BooleanField(verbose_name=_('has met'), default=False)

    def __str__(self):
        return "%s: %s" % (str(self.schedule), self.worker.name)

    def as_dict(self):
        return {
            'title': self.schedule.title,
            'date': str(self.schedule.date),
            'start_time': str(self.schedule.start_time),
            'end_time': str(self.schedule.end_time),
            'has_met': self.has_met,
            'description': self.schedule.description
        }
