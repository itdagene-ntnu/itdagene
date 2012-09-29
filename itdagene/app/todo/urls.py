from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('itdagene.app.todo.views',
    (r'^add/$', 'add_todo'),
    url(r'^add/collective/$', 'add_collective_todo', name='add_collective_todo'),
    (r'^done/$', 'done_todo'),

)