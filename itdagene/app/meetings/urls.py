from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'itdagene.app.meetings.views.list', name='meetings'),
    url(r'^add$', 'itdagene.app.meetings.views.add'),
    url(r'^(?P<id>\d+)/$', 'itdagene.app.meetings.views.meeting', name="view_meeting"),
    url(r'^(?P<id>\d+)/add-penalty$', 'itdagene.app.meetings.views.add_penalties'),
    url(r'^(?P<id>\d+)/edit$', 'itdagene.app.meetings.views.edit'),
    url(r'^(?P<id>\d+)/attend$', 'itdagene.app.meetings.views.attend'),
    url(r'^(?P<id>\d+)/not-attend$', 'itdagene.app.meetings.views.not_attend'),
    url(r'^(?P<id>\d+)/send-invites$', 'itdagene.app.meetings.views.send_invites'),
]
