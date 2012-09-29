from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('itdagene.app.events.views',
    url(r'^$', 'list_events', name='events'),
    url(r'^add/$', 'edit_event', name='add_event'),
    url(r'^(?P<id>\d+)/$', 'view_event', name='view_event'),
    url(r'^(?P<id>\d+)/edit/$', 'edit_event', name='edit_event'),
    url(r'^ticket/(?P<id>\d+)/edit/$', 'edit_ticket', name='edit_ticket'),
)
