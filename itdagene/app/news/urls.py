from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('itdagene.app.news.views',
    url(r'^add/$', 'create_announcement', name='create_announcement'),
    url(r'^(?P<id>\d+)/$', 'view_announcement', name='view_announcement'),
    url(r'^(?P<id>\d+)/edit/$', 'edit_announcement'),
)