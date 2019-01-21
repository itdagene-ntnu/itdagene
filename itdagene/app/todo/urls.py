from django.urls import re_path
from itdagene.app.todo.views import (
    add_todo,
    change_status,
    change_todo,
    delete_todo,
    view_todo,
)

urlpatterns = [
    re_path(r"add/$", add_todo, name="itdagene.todo.add_todo"),
    re_path(r"^(?P<pk>\d+)/change/$", change_todo, name="itdagene.todo.change_todo"),
    re_path(r"^(?P<pk>\d+)/delete/$", delete_todo, name="itdagene.todo.delete_todo"),
    re_path(
        r"^(?P<pk>\d+)/change/status/$",
        change_status,
        name="itdagene.todo.change_status",
    ),
    re_path(r"^(?P<pk>\d+)/$", view_todo, name="itdagene.todo.view_todo"),
]
