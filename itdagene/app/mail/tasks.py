# -*- coding: utf8 -*-

from celery import task

from .senders import meeting_send_invite as msi


@task()
def meeting_send_invite(users, meeting):
    msi(users, meeting)
