from django.conf.urls import url

from itdagene.app.news.views import admin, create_announcement, edit_announcement

urlpatterns = [
    url(r'^add/$', create_announcement, name='itdagene.app.news.views.create_announcement'),
    url(r'^$', admin, name='itdagene.app.news.views.admin'),
    url(
        r'^(?P<id>\d+)/edit/$', edit_announcement, name='itdagene.app.news.views.edit_announcement'
    ),
]
