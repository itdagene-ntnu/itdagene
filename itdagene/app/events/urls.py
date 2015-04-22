from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'itdagene.app.events.views.list_events'),
    url(r'^add/$', 'itdagene.app.events.views.add_event'),
    url(r'^(?P<pk>\d+)/$', 'itdagene.app.events.views.view_event'),
    url(r'^(?P<pk>\d+)/edit/$', 'itdagene.app.events.views.edit_event'),
    url(r'^ticket/(?P<pk>\d+)/edit/$', 'itdagene.app.events.views.edit_ticket'),
]
