from django.conf.urls import patterns, url

urlpatterns = patterns('itdagene.app.meetings.views',
                       url(r'^$', 'list', name='meetings'),
                       url(r'^add$', 'add'), url(r'^(?P<id>\d+)/$', 'meeting', name="view_meeting"),
                       url(r'^(?P<id>\d+)/add-penalty$', 'add_penalties'),
                       url(r'^(?P<id>\d+)/edit$', 'edit'),
                       url(r'^(?P<id>\d+)/attend$', 'attend'),
                       url(r'^(?P<id>\d+)/not-attend$', 'not_attend'),
                       url(r'^(?P<id>\d+)/send-invites$', 'send_invites'), )
