from django.conf.urls import url

from itdagene.app.workschedule import views

urlpatterns = [
    url(r'^$', views.list, name='workschedules'),
    url(r'^add_task$', views.add_task, name='itdagene.app.workschedule.views.add_task'),
    url(r'^add_worker$', views.add_worker, name='itdagene.app.workschedule.views.add_worker'),
    url(r'^task/(?P<id>\d+)/$', views.view_task, name='itdagene.app.workschedule.views.view_task'),
    url(
        r'^task/(?P<id>\d+)/edit$', views.edit_task,
        name='itdagene.app.workschedule.views.edit_task'
    ),
    url(
        r'^worker/(?P<id>\d+)/$', views.view_worker,
        name='itdagene.app.workschedule.views.view_worker'
    ),
    url(
        r'^worker/(?P<id>\d+)/edit$', views.edit_worker,
        name='itdagene.app.workschedule.views.edit_worker'
    ),
    url(
        r'^task/attendance/(?P<id>\d+)$', views.change_attendance,
        name='itdagene.app.workschedule.views.change_attendance'
    ),
]
