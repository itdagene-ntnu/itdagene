from django.db import models
from django.contrib.auth.models import Group
from itdagene.core.models import BaseModel, User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models import Q
from django.core.urlresolvers import reverse


class MailMapping(BaseModel):
    address = models.CharField(max_length=100, verbose_name=_("Address"), unique=True)
    users = models.ManyToManyField(User, blank=True, null=True, verbose_name=_('Users'), related_name='user_mail_mappings')
    groups = models.ManyToManyField(Group, blank=True, null=True, verbose_name=_('Groups'), related_name='group_mail_mappings')
    recived_emails = models.IntegerField(max_length=9999999, verbose_name=_('Recived emails'), default=0)

    class Meta:
        permissions = (
            ("mail_access", "Can access mail app"),
        )


    @classmethod
    def get_group_mappings(cls, group):
        return cls.objects.filter(groups__in=[group]).order_by('address')


    @classmethod
    def get_user_mappings(cls, user):
        return cls.objects.filter(Q(users__in=[user]) | Q(groups__in=[group for group in user.groups.all()])).distinct().order_by('address')


    def all_users(self):
        users = []
        groups = self.groups.all()
        for group in groups:
            [users.append(user) for user in group.user_set.all()]
        [users.append(user) for user in self.users.all()]
        return set(users)


    @classmethod
    def get_destinations_and_headers(cls, address, domain):

        result = {
            'addresses': [],
            'headers': {
                'Precedence': 'List',
                'List-Id': "%s@%s" % (address, domain),
                'X-Mail-Processor': '%s mail' % (settings.SITE['name'], ),
                'List-Unsubscribe': '<http://%s> - Contact admin to disable mail.' % (settings.SITE['domain'], ),
                'List-Post': "<mailto:%s@%s>" % (address, domain)
            }
        }

        # Check private usermails
        try:
            user_with_mapping = User.objects.get(mail_prefix=address)
            if user_with_mapping:
                if user_with_mapping.mail_prefix:
                    result['addresses'] = [ user_with_mapping.email ]
                    return result
        except:
            pass

        mappings = cls.objects.filter(address=address)
        # User mail not match someone, return mappings
        for mapping in mappings:
            added_addresses = False
            for user_addresses in mapping.all_users():
                result['addresses'].append(user_addresses.email)
                added_addresses = True
            if added_addresses:
                mapping.recived_emails += 1
                mapping.save(notify_subscribers=False)
        return result


    def get_absolute_url(self):
        return reverse('itdagene.app.mail.views.view_mailmapping', args=[self.pk])

    def __unicode__(self):
        return '%s@%s' % (self.address, settings.SITE['domain'])


class RestrictedMapping(models.Model):
    users = models.ManyToManyField(User, blank=True, verbose_name=_('Users'))
    groups = models.ManyToManyField(Group, blank=True, verbose_name=_('Groups'))
    token = models.CharField(max_length=70, verbose_name=_("Token"))
    from_address = models.EmailField(null=True, verbose_name=_("From address"))
    timeout = models.DateTimeField(auto_now=True, verbose_name=_("Timeout"))