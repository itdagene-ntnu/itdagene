from django.urls import re_path

from itdagene.app.meetings.views import (
    add, add_penalties, attend, edit, list, meeting, not_attend, send_invites
)

urlpatterns = [
    re_path(r'^$', list, name='meetings'),
    re_path(r'^add$', add, name='itdagene.app.meetings.views.add'),
    re_path(r'^(?P<id>\d+)/$', meeting, name="view_meeting"),
    re_path(r'^(?P<id>\d+)/add-penalty$', add_penalties),
    re_path(r'^(?P<id>\d+)/edit$', edit),
    re_path(r'^(?P<id>\d+)/attend$', attend),
    re_path(r'^(?P<id>\d+)/not-attend$', not_attend),
    re_path(r'^(?P<id>\d+)/send-invites$', send_invites),
]
