from django.conf.urls import patterns, url

urlpatterns = patterns('itdagene.app.todo.views',
    url(r'add/$', 'add_todo'),
    url(r'^(?P<pk>\d+)/change/$', 'change_todo'),
    url(r'^(?P<pk>\d+)/delete/$', 'delete_todo'),
    url(r'^(?P<pk>\d+)/change/status/$', 'change_status'),
    url(r'^(?P<pk>\d+)/$', 'view_todo'),
)