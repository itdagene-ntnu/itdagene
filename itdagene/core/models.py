# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _
from itdagene.core.auth import get_current_user
from django.conf import settings
from django.core.urlresolvers import reverse
from datetime import date


class User(AbstractUser):
    phone = models.IntegerField(blank=True, null=True, verbose_name=_('phone number'))
    photo = models.ImageField(upload_to='photos/users/', blank=True, null=True)
    language = models.CharField(max_length=3, default=settings.DEFAULT_LANGUAGE, choices=settings.LANGUAGES)
    mail_prefix = models.CharField(max_length=40, default="", verbose_name=_('Mail prefix'), help_text=_('This is a mail prefix for your itdagene mail. The address will be value@itdagene.no. This is typicaly you name or username. Don\'t use a group name.'), unique=True)
    mail_notification = models.BooleanField(default=True, verbose_name=_('Send mail notifications'))
    year = models.PositiveIntegerField(verbose_name=_('Active Year'), help_text=_('Year the user was active.'), max_length=3000, default=date.today().year)

    def mail_mappings(self):
        from itdagene.app.mail.models import MailMapping
        return MailMapping.get_user_mappings(self)

    class Meta(AbstractUser.Meta):
        permissions = (("send_welcome_email", "Can send welcome emails"),)

    def get_absolute_url(self):
        return reverse('itdagene.app.users.views.user_detail', args=[self.pk])

    def __unicode__(self):
        if self.get_full_name():
            return self.get_full_name()
        return self.username


class UserProxy(User):
    """
    Brukes av api for å generere liste med brukere.
    """
    class Meta:
        proxy = True

    def as_dict(self):
        return {
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }


class BaseModel(models.Model):
    creator = models.ForeignKey(User, editable=False, related_name="%(class)s_creator")
    saved_by = models.ForeignKey(User, editable=False, related_name="%(class)s_saved_by")
    date_created = models.DateTimeField(editable=False)
    date_saved = models.DateTimeField(editable=False)

    def __unicode__(self):
        return self.creator.username + ' ' + str(self.id)

    def save(self, notify_subscribers=True, log_it=True, log_priority=0, *args, **kwargs):
        user = get_current_user()
        action = 'EDIT' if self.pk else 'CREATE'

        if not user or not user.is_authenticated():
            user = User.objects.get(pk=1)
        if not self.pk:
            self.creator = user

        self.saved_by = user

        if not self.pk:
            self.date_created = datetime.now()

        self.date_saved = datetime.now()

        super(BaseModel, self).save(*args, **kwargs)

        from itdagene.core.notifications.models import Subscription
        Subscription.subscribe(self, user)

        if notify_subscribers:
            Subscription.notify_subscribers(self)

        if log_it:
            from itdagene.core.log.models import LogItem
            LogItem.log_it(self, action, log_priority)


    def get_absolute_url(self):
        c_type = ContentType.objects.get_for_model(self)
        return '/%s/%ss/%s/' % (str(c_type.app_label), str(c_type), str(self.pk))

    def notification_priority(self):
        return 1

    def notification_message(self):
        return '%s was changed' % str(self)

    def notification_object(self):
        return self

    def reset_cache(self):
        key = str(ContentType.objects.get_for_model(self)).replace(' ', '')
#        cache.set(key, list(self.__class__().objects.all()))

    class Meta:
        abstract = True

    @classmethod
    def exclude_fields(cls):
        return None


class Preference(BaseModel):
    display_getting_started = models.BooleanField(default=True, verbose_name=_('Display getting started in admin menu'), help_text=_('When this setting is enabled a getting started element is visible in the admin menu. This contains usefull information about how to use this site.'))
    development_mode = models.BooleanField(default=False, verbose_name=_('Development Mode'), help_text=_('This option puts the site in development mode. The public page will be disabled.'))

    active = models.BooleanField(verbose_name=_('active'), default=False)
    year = models.IntegerField(blank=True, null=True, verbose_name=_('year'))
    start_date = models.DateField(verbose_name=_('start date'))
    end_date = models.DateField(verbose_name=_('end date'))
    nr_of_stands = models.PositiveIntegerField(default=30, verbose_name=_('number of stands'),
                                               help_text=_('This is for each day, not the sum of each day'))
    view_sp = models.BooleanField(verbose_name=_('view partners'), default=False)

    def __unicode__(self):
        return str(self.year)

    def save(self, *args, **kwargs):
        action = 'EDIT' if self.pk else 'CREATE'

        super(Preference, self).save(*args, **kwargs)
        from log.models import LogItem
        LogItem.log_it(self, action, 3)

        if self.active:
            cache.set('pref', self)

    class Meta:
        verbose_name = _('Preference')
        verbose_name_plural = _('Preferences')

    @classmethod
    def current_preference(cls):
        if cache.get('pref'):
            pref = cache.get('pref')
        else:
            try:
                pref = Preference.objects.get(active=True)
            except Preference.DoesNotExist:
                year = datetime.now().year
                pref, created = Preference.objects.get_or_create(year=year, defaults={'active':True, 'start_date':'%s-09-10' % year, 'end_date':'%s-09-11' % year})
                pref.active = True
                pref.save(notify_subscribers=False, log_it=False)
            cache.set('pref', pref)
        return pref

    @classmethod
    def get_preference_by_year(cls, year):
        try:
            pref = cls.objects.get(year=int(year), active=True)
            return pref
        except:
            year = datetime.now().year
            pref, created = Preference.objects.get_or_create(year=year, defaults={'active':True, 'start_date':'%s-09-10' % year, 'end_date':'%s-09-11' % year})
            pref.active = True
            pref.save(notify_subscribers=False, log_it=False)
            return pref

    def get_absolute_url(self):
        return reverse('itdagene.app.admin.views.preferences.edit')
