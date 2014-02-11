from datetime import datetime
from itdagene.core.auth import get_current_user
from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from itdagene.core.log.models import LogItem
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


class BaseModel(models.Model):
    creator = models.ForeignKey(User, editable=False, related_name="%(class)s_creator")
    saved_by = models.ForeignKey(User, editable=False, related_name="%(class)s_saved_by")
    date_created = models.DateTimeField(editable=False)
    date_saved = models.DateTimeField(editable=False)

    def __unicode__(self):
        return self.creator.username + ' ' + str(self.id)

    def save(self, notify_subscribers=True, *args, **kwargs):
        user = get_current_user()
        if not user or not user.is_authenticated():
            user = User.objects.get(pk=1) #dummy user
        if not self.pk: self.creator = user
        self.saved_by = user
        if not self.pk: self.date_created = datetime.now()
        self.date_saved = datetime.now()
        super(BaseModel, self).save(*args,**kwargs)
        Subscription.subscribe(self, user)
        if notify_subscribers: Subscription.notify_subscribers(self)
        self.reset_cache()

    def get_absolute_url(self):
        c_type = ContentType.objects.get_for_model(self)
        return '/%s/%ss/%s/' % (str(c_type.app_label), str(c_type), str(self.pk))

    def notification_priority(self): return 1
    def notification_message(self): return '%s was changed' % str(self)
    def notification_template(self): return 'emails/notifications/base.html'
    def notification_object(self): return self

    def reset_cache(self):
        key = str(ContentType.objects.get_for_model(self)).replace(' ', '')
#        cache.set(key, list(self.__class__().objects.all()))

    class Meta:
        abstract = True

    @classmethod
    def exclude_fields(cls):
        return None


class Preference(BaseModel):
    active = models.BooleanField(verbose_name=_('active'))
    year = models.IntegerField(blank=True,null=True,verbose_name=_('year'))
    start_date = models.DateField(verbose_name=_('start date'))
    end_date = models.DateField(verbose_name=_('end date'))
    nr_of_stands = models.PositiveIntegerField(default=30,verbose_name=_('number of stands'), help_text=_('This is for each day, not the sum of each day'))
    view_sp = models.BooleanField(verbose_name=_('view partners'))

    def __unicode__(self):
        return str(self.year)

    def save(self, *args, **kwargs):
        if self.pk: action = 'EDIT'
        else: action = 'CREATE'
        super(Preference, self).save(*args, **kwargs)
        LogItem.log_it(self, action, 3)
        if self.active: cache.set('pref',self)

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
                pref = Preference.objects.create(active=True, year=year, start_date='%s-09-10' % year, end_date='%s-09-11' % year)
            cache.set('pref', pref)
        return pref

class UserProxy(User):
    class Meta:
        proxy = True

    def as_dict(self):
        return {
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }

from itdagene.core.notifications.models import Subscription