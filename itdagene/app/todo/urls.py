from django.conf.urls import url

from itdagene.app.todo.views import add_todo, change_status, change_todo, delete_todo, view_todo

urlpatterns = [
    url(r'add/$', add_todo, name='itdagene.app.todo.views.add_todo'),
    url(r'^(?P<pk>\d+)/change/$', change_todo, name='itdagene.app.todo.views.change_todo'),
    url(r'^(?P<pk>\d+)/delete/$', delete_todo, name='itdagene.app.todo.views.delete_todo'),
    url(
        r'^(?P<pk>\d+)/change/status/$', change_status, name='itdagene.app.todo.views.change_status'
    ),
    url(r'^(?P<pk>\d+)/$', view_todo, name='itdagene.app.todo.views.view_todo'),
]
