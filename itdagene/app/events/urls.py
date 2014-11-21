from django.conf.urls import patterns, url

urlpatterns = patterns('itdagene.app.events.views',
    url(r'^$', 'list_events'),
    url(r'^add/$', 'add_event'),
    url(r'^(?P<pk>\d+)/$', 'view_event'),
    url(r'^(?P<pk>\d+)/edit/$', 'edit_event'),
    url(r'^ticket/(?P<pk>\d+)/edit/$', 'edit_ticket'),
)
