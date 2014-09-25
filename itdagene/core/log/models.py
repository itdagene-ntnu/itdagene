from datetime import datetime
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.mail import send_mail
from itdagene.core.auth import get_current_user
from django.conf import settings
from itdagene.core.models import User

class LogItem (models.Model):

    PRIORITIES = ((0, 'Low'),
                  (1, 'Medium'),
                  (2, 'High'),
                  (3, 'Very High. Will send email to administrators'))

    user = models.ForeignKey(User, verbose_name=_('user'))
    priority = models.PositiveIntegerField(choices=PRIORITIES, default=1,verbose_name=_('priority'))
    timestamp = models.DateTimeField(auto_now=True, verbose_name=_('date'))
    action = models.CharField(max_length=16,verbose_name=_('action'))
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.user.username + '-' + \
               self.action + '-' + \
               ' (' + str(self.content_type) + ')'

    def save(self, *args, **kwargs):
        if self.priority == 3:
                send_mail('[itDAGENE] Log: ' + unicode(self),
                          unicode(self) + '\n read more at http://itdagene.no',
                          settings.FROM_ADDRESS,
                          settings.ADMIN_EMAILS)
                self.sent_mail = True
        super(LogItem, self).save(*args, **kwargs)

    @classmethod
    def log_it(cls, object, action, priority):
        user = get_current_user()
        if not user or  not user.is_authenticated():
            user = User.objects.get(pk=1)
        l = LogItem(
            user=user,
            priority=priority,
            timestamp=datetime.now(),
            action=action,
            object_id=object.pk,
            content_type=ContentType.objects.get_for_model(object)
        )
        l.save()
