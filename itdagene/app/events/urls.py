from django.conf.urls import url
from itdagene.app.events.views import list_events, add_event, edit_event, view_event, edit_ticket

urlpatterns = [
    url(r'^$', list_events, name='itdagene.app.events.views.list_events'),
    url(r'^add/$', add_event, name='itdagene.app.events.views.add_event'),
    url(r'^(?P<pk>\d+)/$', view_event, name='itdagene.app.events.views.view_event'),
    url(r'^(?P<pk>\d+)/edit/$', edit_event, name='itdagene.app.events.views.edit_event'),
    url(r'^ticket/(?P<pk>\d+)/edit/$', edit_ticket, name='itdagene.app.events.views.edit_ticket'),
]

