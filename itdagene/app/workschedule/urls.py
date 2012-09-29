from django.conf.urls import patterns, url

urlpatterns = patterns('itdagene.app.workschedule.views',
    url(r'^$', 'list', name='workschedules'),
    (r'^emails$', 'email_list'),
    (r'^add$', 'add'),
    (r'^(?P<id>\d+)/edit$', 'has_met'),
    (r'^has_met/(?P<id>\d+)/$', 'has_met'),
)
