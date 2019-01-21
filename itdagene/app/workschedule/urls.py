from django.urls import re_path
from itdagene.app.workschedule import views

urlpatterns = [
    # re_path(r'^$', views.list, name='itdagene.workschedule.list'),
    re_path(r"^add_task$", views.add_task, name="itdagene.workschedule.add_task"),
    re_path(r"^add_worker$", views.add_worker, name="itdagene.workschedule.add_worker"),
    re_path(
        r"^task/(?P<id>\d+)/$", views.view_task, name="itdagene.workschedule.view_task"
    ),
    re_path(
        r"^task/(?P<id>\d+)/edit$",
        views.edit_task,
        name="itdagene.workschedule.edit_task",
    ),
    # re_path(r'^worker/(?P<id>\d+)/$', views.view_worker, name='itdagene.workschedule.view_worker')
    re_path(
        r"^worker/(?P<id>\d+)/edit$",
        views.edit_worker,
        name="itdagene.workschedule.edit_worker",
    ),
    re_path(
        r"^task/attendance/(?P<id>\d+)$",
        views.change_attendance,
        name="itdagene.workschedule.change_attendance",
    ),
]
