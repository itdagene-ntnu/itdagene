from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from itdagene.app.company.models import Company, CompanyContact
from itdagene.core.models import BaseModel

from .managers import JoblistingManager


class Town(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_('name'))

    def __str__(self):
        return self.name


class Joblisting(BaseModel):

    objects = JoblistingManager()
    all_objects = models.Manager()

    JOB_TYPES = (
        ('si', _('Summer internship')),
        ('pp', _('Permanent position')),
    )

    company = models.ForeignKey(
        Company,
        related_name='joblistings',
        verbose_name=_('company'),
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=160, verbose_name=_('title'))
    type = models.CharField(max_length=20, choices=JOB_TYPES, verbose_name=_('type'))
    description = models.TextField(verbose_name=_('Description'))
    contact = models.ForeignKey(
        CompanyContact,
        null=True,
        blank=True,
        verbose_name=_('contact'),
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        upload_to='joblistings/', null=True, blank=True, verbose_name=_('image')
    )
    deadline = models.DateTimeField(null=True, blank=True, verbose_name=_('deadline'))
    from_year = models.PositiveIntegerField(default=1, verbose_name=_('from year'))
    to_year = models.PositiveIntegerField(default=5, verbose_name=_('to year'))
    towns = models.ManyToManyField(Town, blank=True, verbose_name=_('town'))
    url = models.URLField(blank=True, verbose_name=_('url'))
    is_active = models.BooleanField(verbose_name=_('active'), default=True)
    frontpage = models.BooleanField(_('Frontpage'), default=False)
    hide_contactinfo = models.BooleanField(_('Hide contact info'), default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('itdagene.career.view', args=[self.pk])

    def has_deadline_passed(self):
        return self.deadline < timezone.now()

    def get_towns(self):
        def get_name(town):
            return town.name

        towns = map(get_name, self.towns.all())
        return ', '.join(towns)

    def get_classes(self):
        if self.from_year != self.to_year:
            return '%s-%s' % (self.from_year, self.to_year)
        return self.to_year

    class Meta:
        ordering = ('deadline', )
        base_manager_name = 'objects'
