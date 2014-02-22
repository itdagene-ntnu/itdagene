from datetime import datetime
from django.core.cache import cache
from django.db import models
from itdagene.core.log.models import LogItem
from itdagene.core.models import BaseModel, Preference
from django.contrib.auth.models import User
from itdagene.core.util import expire_page_cache
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

class BoardPosition (BaseModel):
    title = models.CharField(max_length=100, verbose_name=_('title'))
    email = models.EmailField(blank=True, null=True, default='',verbose_name=_('email'))

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk: action = 'EDIT'
        else: action = 'CREATE'
        super(BoardPosition, self).save(*args, **kwargs)
        LogItem.log_it(self, action, 1)

    class Meta:
        verbose_name = _('Boardposition')
        verbose_name_plural = _('Boardpositions')


class Profile (BaseModel):
    user = models.OneToOneField(User, related_name='profile', verbose_name=_('user'))
    type = models.CharField(max_length=1, choices=settings.PROFILE_TYPES, default='u', verbose_name=_('type'))
    position = models.ForeignKey(BoardPosition, blank=True, null=True,verbose_name=_('position'))
    year = models.IntegerField(blank=True,null=True,verbose_name=_('year'), help_text=_('The year this person arranged itDAGENE'))
    phone = models.IntegerField(blank=True,null=True,verbose_name=_('phone number'))
    language = models.CharField(max_length=3, default=settings.DEFAULT_LANGUAGE, choices=settings.LANGUAGES)
    photo = models.ImageField(upload_to='photos/profiles/', blank=True, null=True)
    mail_notification = models.BooleanField(default=True, verbose_name=_('mail notification'),
                                            help_text=_('If you uncheck this the website will not send email you notifications.'))

    def __unicode__(self):
        return self.user.get_full_name()

    def is_board_member(self):
        return self.type == 'b'

    def save(self, *args, **kwargs):
        if self.pk: action = 'EDIT'
        else: action = 'CREATE'
        super(Profile, self).save(*args, **kwargs)
        if self.type == 'b': LogItem.log_it(self, action, 1)
        else: LogItem.log_it(self, action, 0)
        cache.delete('profile' + str(self.user.pk))
        cache.set('profileccount', Profile.objects.filter(type='c').count())
        cache.set('profileucount', Profile.objects.filter(type='u').count())
        cache.set('profilewcount', Profile.objects.filter(type='w').count())
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
