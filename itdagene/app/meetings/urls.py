from django.conf.urls import url

from itdagene.app.meetings.views import (
    add, add_penalties, attend, edit, meeting, not_attend, send_invites
)

urlpatterns = [
    url(r'^$', list, name='meetings'),
    url(r'^add$', add, name='itdagene.app.meetings.views.add'),
    url(r'^(?P<id>\d+)/$', meeting, name="view_meeting"),
    url(r'^(?P<id>\d+)/add-penalty$', add_penalties),
    url(r'^(?P<id>\d+)/edit$', edit),
    url(r'^(?P<id>\d+)/attend$', attend),
    url(r'^(?P<id>\d+)/not-attend$', not_attend),
    url(r'^(?P<id>\d+)/send-invites$', send_invites),
]
