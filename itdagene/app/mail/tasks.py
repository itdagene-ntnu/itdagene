# -*- coding: utf8 -*-

from django.conf import settings
from django.core.mail import mail_admins

from itdagene.celery import app

from .senders import meeting_send_invite as msi
from .senders import notifications_send_email as nse
from .senders import send_comment_email as ce


@app.task(bind=True)
def meeting_send_invite(self, users, meeting):
    msi(users, meeting)


@app.task(bind=True)
def send_notification_message(self, notification):
    nse(notification)


@app.task(bind=True)
def send_comment_email(self, comment):
    ce(comment)


@app.task(bind=True)
def send_admin_mail(self, log_item):
    mail_admins(
        'Log: ' + str(log_item),
        str(log_item) + '\n Read more at http://{}{}'.format(
            settings.SITE['domain'], log_item.content_object.get_absolute_url()
        )
    )
