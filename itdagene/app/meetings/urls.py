from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('itdagene.app.meetings.views',
            url(r'^$', 'list', name='meetings'),
            url(r'^add$', 'add'),
            url(r'^search', 'search'),
            url(r'^(?P<id>\d+)/$', 'meeting'),
            url(r'^(?P<id>\d+)/edit$', 'edit'),
            url(r'^(?P<id>\d+)/attend$', 'attend'),
            url(r'^(?P<id>\d+)/not-attend$', 'not_attend'),
            url(r'^(?P<id>\d+)/send-invites$', 'send_invites'),
)