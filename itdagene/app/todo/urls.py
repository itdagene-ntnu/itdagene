from django.conf.urls import url

urlpatterns = [
    url(r'add/$', 'itdagene.app.todo.views.add_todo'),
    url(r'^(?P<pk>\d+)/change/$', 'itdagene.app.todo.views.change_todo'),
    url(r'^(?P<pk>\d+)/delete/$', 'itdagene.app.todo.views.delete_todo'),
    url(r'^(?P<pk>\d+)/change/status/$', 'itdagene.app.todo.views.change_status'),
    url(r'^(?P<pk>\d+)/$', 'itdagene.app.todo.views.view_todo'),
]
