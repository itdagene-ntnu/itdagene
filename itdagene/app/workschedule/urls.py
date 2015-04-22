from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'itdagene.app.workschedule.views.list', name='workschedules'),
    url(r'^add_task$', 'itdagene.app.workschedule.views.add_task'),
    url(r'^add_worker$', 'itdagene.app.workschedule.views.add_worker'),
    url(r'^task/(?P<id>\d+)/$', 'itdagene.app.workschedule.views.view_task'),
    url(r'^task/(?P<id>\d+)/edit$', 'itdagene.app.workschedule.views.edit_task'),
    url(r'^worker/(?P<id>\d+)/$', 'itdagene.app.workschedule.views.view_worker'),
    url(r'^worker/(?P<id>\d+)/edit$', 'itdagene.app.workschedule.views.edit_worker'),
    url(r'^task/attendance/(?P<id>\d+)$', 'itdagene.app.workschedule.views.change_attendance'),
]
