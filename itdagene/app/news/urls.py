from django.conf.urls import patterns, url

urlpatterns = patterns('itdagene.app.news.views',
                       url(r'^add/$', 'create_announcement',
                           name='create_announcement'), url(r'^$', 'admin'),
                       url(r'^(?P<id>\d+)/edit/$', 'edit_announcement'), )
