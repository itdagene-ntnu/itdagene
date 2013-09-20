from django.conf.urls import patterns, url

urlpatterns = patterns('itdagene.app.workschedule.views',
    url(r'^$', 'list', name='workschedules'),
    (r'^emails$', 'email_list'),
    (r'^add_workschedule$', 'add_workschedule'),
    (r'^add_worker$', 'add_worker'),
    (r'^(?P<id>\d+)/$', 'view_task'),
    (r'^(?P<id>\d+)/$', 'view_worker'),
    (r'^(?P<id>\d+)/edit$', 'has_met'),
    (r'^has_met/(?P<id>\d+)/$', 'has_met'),
)
