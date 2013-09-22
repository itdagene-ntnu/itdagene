from django.conf.urls import patterns, url

urlpatterns = patterns('itdagene.app.workschedule.views',
    url(r'^$', 'list', name='workschedules'),
    (r'^emails$', 'email_list'),
    (r'^add_task$', 'add_task'),
    (r'^add_worker$', 'add_worker'),
    (r'^task/(?P<id>\d+)/$', 'view_task'),
    (r'^task/(?P<id>\d+)/edit$', 'edit_task'),
    (r'^worker/(?P<id>\d+)/$', 'view_worker'),
    (r'^worker/(?P<id>\d+)/edit$', 'edit_worker'),
    (r'^task/(?P<id>\d+)/attendance$', 'has_met'),
)
