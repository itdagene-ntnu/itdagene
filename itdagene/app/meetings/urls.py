from django.urls import re_path
from itdagene.app.meetings.views import (
    add,
    add_penalties,
    attend,
    edit,
    list,
    meeting,
    not_attend,
    send_invites,
)

urlpatterns = [
    re_path(r"^$", list, name="itdagene.meetings.list"),
    re_path(r"^add$", add, name="itdagene.meetings.add"),
    re_path(r"^(?P<id>\d+)/$", meeting, name="itdagene.meetings.meeting"),
    re_path(
        r"^(?P<id>\d+)/add-penalty$",
        add_penalties,
        name="itdagene.meetings.add_penalties",
    ),
    re_path(r"^(?P<id>\d+)/edit$", edit, name="itdagene.meetings.edit"),
    re_path(r"^(?P<id>\d+)/attend$", attend, name="itdagene.meetings.attend"),
    re_path(
        r"^(?P<id>\d+)/not-attend$", not_attend, name="itdagene.meetings.not_attend"
    ),
    re_path(
        r"^(?P<id>\d+)/send-invites$",
        send_invites,
        name="itdagene.meetings.send_invites",
    ),
]
