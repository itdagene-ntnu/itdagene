# -*- coding: utf8 -*-

from celery import task

from .senders import meeting_send_invite as msi
from .senders import notifications_send_email as nse
from .senders import send_comment_email as ce


@task()
def meeting_send_invite(users, meeting):
    msi(users, meeting)


@task()
def send_notification_message(notification):
    nse(notification)


@task()
def send_comment_email(comment):
    ce(comment)
