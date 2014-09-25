from django.db import models
from django.contrib.auth.models import Group
from itdagene.core.models import BaseModel, User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models import Q

class MailMapping(models.Model):
    address = models.CharField(max_length=100, verbose_name=_("Address"), unique=True)
    users = models.ManyToManyField(User, blank=True, null=True, verbose_name=_('Users'), related_name='mail_mappings')
    groups = models.ManyToManyField(Group, blank=True, null=True, verbose_name=_('Groups'), related_name='mail_mappings')
    recived_emails = models.IntegerField(max_length=9999999, verbose_name=_('Recived emails'), default=0)

    class Meta:
        permissions = (
            ("mail_access", "Can access mail app"),
        )


    @classmethod
    def get_group_mappings(cls, group):
        return cls.objects.filter(groups=group).order_by('address')


    def all_users(self):
        users = []
        groups = self.groups.all()
        for group in groups:
            [users.append(user) for user in group.user_set.all()]
        [users.append(user) for user in self.users.all()]

        return set(users)


    def __unicode__(self):
        return '%s@%s' % (self.address, settings.SITE['domain'])


class RestrictedMapping(models.Model):
    users = models.ManyToManyField(User, blank=True, verbose_name=_('Users'))
    groups = models.ManyToManyField(Group, blank=True, verbose_name=_('Groups'))
    token = models.CharField(max_length=70, verbose_name=_("Token"))
    from_address = models.EmailField(null=True, verbose_name=_("From address"))
    timeout = models.DateTimeField(auto_now=True, verbose_name=_("Timeout"))