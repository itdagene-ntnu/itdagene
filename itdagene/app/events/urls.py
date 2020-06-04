from django.urls import re_path
from itdagene.app.events.views import (
    add_event,
    delete_event,
    edit_event,
    edit_ticket,
    list_events,
    view_event,
)

urlpatterns = [
    re_path(r"^$", list_events, name="itdagene.events.list_events"),
    re_path(r"^add/$", add_event, name="itdagene.events.add_event"),
    re_path(r"^(?P<pk>\d+)/$", view_event, name="itdagene.events.view_event"),
    re_path(r"^(?P<pk>\d+)/edit/$", edit_event, name="itdagene.events.edit_event"),
    re_path(
        r"^(?P<pk>\d+)/delete/$", delete_event, name="itdagene.events.delete_event"
    ),
    re_path(
        r"^ticket/(?P<pk>\d+)/edit/$", edit_ticket, name="itdagene.events.edit_ticket"
    ),
]
