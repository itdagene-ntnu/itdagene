from django.urls import re_path

from itdagene.app.experiences import views

urlpatterns = [
    re_path(r'^$', views.list, name='itdagene.app.experiences.views.list'),
    re_path(r'^add$', views.add, name='itdagene.app.experiences.views.add'),
    re_path(r'^(?P<id>\d+)/$', views.view, name='itdagene.app.experiences.views.view'),
    re_path(r'^(?P<id>\d+)/edit$', views.edit, name='itdagene.app.experiences.views.edit'),
]
