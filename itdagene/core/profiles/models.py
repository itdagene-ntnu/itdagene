from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from itdagene.core.log.models import LogItem
from itdagene.core.models import BaseModel, Preference
from itdagene.core.util.cache import expire_page_cache


class BoardPosition (BaseModel):
    title = models.CharField(max_length=100, verbose_name=_('title'))
    email = models.EmailField(blank=True, null=True, default='', verbose_name=_('email'))

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(BoardPosition, self).save(*args, **kwargs)

        action = 'EDIT' if self.pk else 'CREATE'
        LogItem.log_it(self, action, 1)

    class Meta:
        verbose_name = _('Boardposition')
        verbose_name_plural = _('Boardpositions')


class Profile (BaseModel):
    user = models.OneToOneField(User, related_name='profile', verbose_name=_('user'))
    type = models.CharField(max_length=1, choices=settings.PROFILE_TYPES, default='u', verbose_name=_('type'))
    position = models.ForeignKey(BoardPosition, blank=True, null=True, verbose_name=_('position'))
    year = models.IntegerField(blank=True, null=True, verbose_name=_('year'),
                               help_text=_('The year this person arranged itDAGENE'))
    phone = models.IntegerField(blank=True, null=True, verbose_name=_('phone number'))
    language = models.CharField(max_length=3, default=settings.DEFAULT_LANGUAGE, choices=settings.LANGUAGES)
    photo = models.ImageField(upload_to='photos/profiles/', blank=True, null=True)
    mail_notification = models.BooleanField(default=True, verbose_name=_('mail notification'),
                                            help_text=_('If you uncheck this the website will not send email you '
                                                        'notifications.'))

    def __unicode__(self):
        return self.user.get_full_name()

    def is_board_member(self):
        return self.type == 'b'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        action = 'EDIT' if self.pk else 'CREATE'
        priority = 1 if self.type == 'b' else 0
        LogItem.log_it(self, action, priority)

        expire_page_cache('public_profiles')

    @classmethod
    def get_or_create(cls, user):
        try:
            profile = Profile.objects.get(user=user)
        except (TypeError, Profile.DoesNotExist):
            try:
                anononymous_user = User.objects.get(pk=1)

                profile = Profile.objects.create(creator=anononymous_user,
                                                 saved_by=anononymous_user,
                                                 date_created=datetime.now(),
                                                 date_saved=datetime.now(),
                                                 user=user,
                                                 year=Preference.current_preference().year)
            except (TypeError, User.DoesNotExist, Preference.DoesNotExist):
                profile = None

        return profile

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

User.profile = property(lambda u: Profile.get_or_create(user=u))
