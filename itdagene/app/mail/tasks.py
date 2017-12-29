# -*- coding: utf8 -*-

from itdagene.celery import app

from .senders import meeting_send_invite as msi
from .senders import notifications_send_email as nse
from .senders import send_comment_email as ce


@app.task()
def meeting_send_invite(users, meeting):
    msi(users, meeting)


@app.task()
def send_notification_message(notification):
    nse(notification)


@app.task()
def send_comment_email(comment):
    ce(comment)
