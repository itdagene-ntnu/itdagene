from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField

from itdagene.app.company import COMPANY_STATUS
from itdagene.core.log.models import LogItem
from itdagene.core.models import BaseModel, Preference, User


class Package(BaseModel):
    name = models.CharField(max_length=40, verbose_name=_('name'))
    description = models.TextField(verbose_name=_('description'),
                                   help_text=_('This field supports markdown'))
    price = models.PositiveIntegerField(verbose_name=_('price'))
    max = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_('number of packages to sell'))
    has_stand_first_day = models.BooleanField(default=False)
    has_stand_last_day = models.BooleanField(default=False)
    has_waiting_list = models.BooleanField(default=True,
                                           verbose_name=_('has waiting list'))
    includes_course = models.BooleanField(verbose_name=_('includes course'),
                                          default=False)
    is_full = models.BooleanField(verbose_name=_('is full'), default=False)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('itdagene.app.company.views.packages.view',
                       args=[self.pk])

    def get_waiting_list(self):
        waiting_list = self.waiting_list.all()
        return waiting_list

    @classmethod
    def update_available_spots(cls):
        for package in Package.objects.all():
            if package.companies.all().count() >= package.max:
                package.is_full = True
            else:
                package.is_full = False
            package.save(log_it=False, notify_subscribers=False)

    def save(self, log_it=True, *args, **kwargs):
        if not self.pk:
            action = 'CREATE'
        else:
            action = 'EDIT'
        super(Package, self).save(*args, **kwargs)
        if log_it:
            LogItem.log_it(self, action, 2)

    class Meta:
        ordering = ('name', )
        verbose_name = _('package')
        verbose_name_plural = _('packages')


class Company(BaseModel):
    name = models.CharField(max_length=140, verbose_name=_('name'))
    url = models.URLField(blank=True, null=True, verbose_name=_('url'))
    phone = models.CharField(max_length=20,
                             blank=True,
                             null=True,
                             verbose_name=_('Phone'))
    logo = ImageField(upload_to='company_logos/', null=True, blank=True, verbose_name=_('logo'))
    status = models.PositiveIntegerField(choices=COMPANY_STATUS,
                                         default=0,
                                         verbose_name=_('status'))
    contact = models.ForeignKey(User,
                                related_name='contact_for',
                                blank=True,
                                null=True,
                                verbose_name=_('itDAGENE contact'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    package = models.ForeignKey(Package,
                                related_name='companies',
                                blank=True,
                                null=True,
                                verbose_name=_('package'))
    waiting_for_package = models.ManyToManyField(
        Package,
        related_name='waiting_list',
        blank=True,
        null=True,
        verbose_name=_('waiting for package'))
    address = models.TextField(blank=True, verbose_name=_('address'))
    payment_address = models.TextField(blank=True,
                                       verbose_name=_('payment address'))
    fax = models.CharField(max_length=20, blank=True, null=True)
    active = models.BooleanField(default=True, verbose_name=_('active'))
    has_public_profile = models.BooleanField(verbose_name=_('profile'),
                                             default=False)
    is_collaborator = models.BooleanField(verbose_name='collaborator', default=False)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('itdagene.app.company.views.view', args=[self.pk])

    def save(self, *args, **kwargs):
        super(Company, self).save(*args, **kwargs)
        Package.update_available_spots()

    def unfinished_todos(self):
        return self.todos.filter(finished=False)

    class Meta:
        verbose_name = _('company')
        verbose_name_plural = _('companies')
        ordering = ('name', )

    def nr_of_banquet_tickets(self):
        contract = self.latest_contract()
        if contract is not None:
            return contract.banquet_tickets
        return 0

    def nr_of_joblistings(self):
        contract = self.latest_contract()
        if contract:
            return contract.joblistings
        return 0

    def latest_contract(self):
        if self.contracts.all().count():
            return self.contracts.all().order_by('timestamp').reverse()[0]
        return None

    def current_contract(self):
        c = Contract.objects.filter(
            company=self,
            timestamp__year=Preference.current_preference().year)
        if c.count() > 0:
            return c[0]
        return None

    @classmethod
    def get_signed_with_packages(cls):
        return cls.objects.filter(status=3).exclude(package=None).order_by('?')

    @classmethod
    def get_first_day(cls):
        def filter_images(company):
            return bool(company.logo != '')

        return filter(filter_images,
                      cls.get_signed_with_packages().select_related('package')
                      .filter(package__has_stand_first_day=True))

    @classmethod
    def get_last_day(cls):
        def filter_images(company):
            return bool(company.logo != '')

        return filter(filter_images,
                      cls.get_signed_with_packages().select_related('package')
                      .filter(package__has_stand_last_day=True))


class CompanyContact(BaseModel):
    company = models.ForeignKey(Company,
                                related_name='company_contacts',
                                verbose_name=_('company'))
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('e-mail address'), blank=True)
    phone = models.CharField(max_length=20,
                             blank=True,
                             null=True,
                             verbose_name=_('phone number'))
    mobile_phone = models.CharField(max_length=20,
                                    blank=True,
                                    null=True,
                                    verbose_name=_('phone number'))
    position = models.CharField(max_length=60,
                                blank=True,
                                verbose_name=_('position'))

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        if not self.pk:
            action = 'CREATE'
        else:
            action = 'EDIT'
        super(CompanyContact, self).save(*args, **kwargs)
        LogItem.log_it(self, action, 1)

    class Meta:
        verbose_name = _('company contact')
        verbose_name_plural = _('company contacts')
        ordering = ['-pk']


class Contract(BaseModel):
    company = models.ForeignKey(Company,
                                related_name='contracts',
                                verbose_name=_('company'))
    timestamp = models.DateField(
        verbose_name=_('date'),
        help_text=_('Signing date, not uploaded date'))
    file = models.FileField(upload_to='contracts/', verbose_name=_('file'))
    banquet_tickets = models.PositiveIntegerField(
        default=1,
        verbose_name=_('banquet tickets'))
    joblistings = models.PositiveIntegerField(default=2,
                                              verbose_name=_('joblistings'))
    interview_room = models.PositiveIntegerField(
        default=0,
        verbose_name=_('interview room'))
    is_billed = models.BooleanField(verbose_name=_("is billed"), default=False)
    has_paid = models.BooleanField(verbose_name=_("has paid"), default=False)

    def __unicode__(self):
        return str(self.timestamp)

    def save(self, *args, **kwargs):
        super(Contract, self).save(*args, **kwargs)

    def clean_fields(self, exclude=None):
        if getattr(self, 'company', False):
            if self.company.tickets.all().count(
            ) >= self.company.nr_of_banquet_tickets:
                raise ValidationError(
                    'Cannot add more tickets to this company.')
        super(Contract, self).clean_fields(exclude=exclude)

    class Meta:
        verbose_name = _('contract')
        verbose_name_plural = _('contracts')


class CallTeam(BaseModel):
    users = models.ManyToManyField(User, verbose_name=_('users'))

    def __unicode__(self):
        u = []
        for user in self.users.all():
            u.append(user.get_full_name())
        return ", ".join(u)
