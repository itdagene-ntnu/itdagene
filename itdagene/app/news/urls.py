from django.conf.urls import url

urlpatterns = [
    url(r'^add/$', 'itdagene.app.news.views.create_announcement', name='create_announcement'),
    url(r'^$', 'itdagene.app.news.views.admin'),
    url(r'^(?P<id>\d+)/edit/$', 'itdagene.app.news.views.edit_announcement'),
]
