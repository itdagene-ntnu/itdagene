from datetime import datetime
from django.contrib.contenttypes import generic
from django.db import models
from django.utils import translation
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from itdagene.core.models import User
from django.shortcuts import get_object_or_404
from itdagene.core.auth import get_current_user
from itdagene.core.shortcuts import send_language_specific_mail

class Notification (models.Model):

    PRIORITIES = ((0, 'Low'),
                  (1, 'Medium'),
                  (2, 'High'))

    user = models.ForeignKey(User, verbose_name=_('user'))
    priority = models.PositiveIntegerField(choices=PRIORITIES, default=1,verbose_name=_('priority'))
    date = models.DateTimeField(auto_now=True, verbose_name=_('date'))
    message = models.TextField(verbose_name=_('message'))
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    send_mail = models.BooleanField(default=True, verbose_name=_('send mail'))
    sent_mail = models.BooleanField(verbose_name=_('sent mail'), default=False)
    read = models.BooleanField(default=True)

    def __unicode__(self):
        if len(self.message) > 100:
            return '%s: %s...' % (self.user, self.message[0:100])
        return '%s: %s' % (self.user.username, self.message)

    def save(self, mail_template=None, *args, **kwargs):
        if self.send_mail and not self.sent_mail:
            translation.activate(self.user.profile.language)
            if self.user.profile.mail_notification and self.user.email:
                if not mail_template: mail_template=self.content_object.notification_template()
                send_language_specific_mail(
                    subject=_('[itDAGENE] You have a new notification'),
                    user_list=[self.user],
                    template=mail_template,
                    context={'object': self.content_object},
                )
                self.sent_mail=True
        super(Notification, self).save(*args, **kwargs)
        translation.activate(get_current_user().profile.language)

    def read(self):
        self.read = True
        self.save()

    @classmethod
    def notify(cls, object, user, template=None):
        pass
#        s_mail=bool(object.notification_priority())
#        content_type = ContentType.objects.get_for_model(object)
#        if not user == core.get_current_user():
#            n = Notification(user=user,
#                priority=object.notification_priority(),
#                message=object.notification_message(),
#                content_type=content_type,
#                object_id=object.pk,
#                send_mail=s_mail,
#                read=False,
#            )
#            n.save(mail_template=template)

class Subscription (models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='subscriptions')

    @classmethod
    def notify_subscribers(cls, object):
        n_object = ContentType.objects.get_for_model(object.notification_object())
        subscription = get_object_or_404(Subscription, content_type=n_object, object_id=object.notification_object().id)
        for subscriber in subscription.subscribers.all():
            Notification.notify(object, subscriber, template=object.notification_template())

    @classmethod
    def subscribe (cls, object, user):
        subscription = Subscription.get_or_create(object)
        if not user in subscription.subscribers.all(): subscription.subscribers.add(user)
        subscription.save()

    @classmethod
    def get_or_create(cls, object):
        content_type = ContentType.objects.get_for_model(object)
        try:
            subscription = Subscription.objects.get(content_type=content_type, object_id=object.id)
        except (TypeError, Subscription.DoesNotExist):
            subscription = Subscription(content_type=content_type, object_id=object.id)
            subscription.save()
        return subscription