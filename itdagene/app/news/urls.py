from django.urls import re_path

from itdagene.app.news.views import admin, create_announcement, edit_announcement

urlpatterns = [
    re_path(r'^add/$', create_announcement, name='itdagene.app.news.views.create_announcement'),
    re_path(r'^$', admin, name='itdagene.app.news.views.admin'),
    re_path(
        r'^(?P<id>\d+)/edit/$', edit_announcement, name='itdagene.app.news.views.edit_announcement'
    ),
]
