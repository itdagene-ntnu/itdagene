from django.urls import re_path

from itdagene.app.career import views

urlpatterns = [
    re_path(r'^joblistings/$', views.list, name='itdagene.app.career.views.list'),
    re_path(r'^joblistings/add/$', views.add, name='itdagene.app.career.views.add'),
    re_path(r'^joblistings/(?P<pk>\d+)/$', views.view),
    re_path(r'^joblistings/(?P<pk>\d+)/edit/$', views.edit),
    re_path(r'^joblistings/(?P<pk>\d+)/delete/$', views.delete),
    re_path(r'^joblistings/add_town/$', views.add_town, name='itdagene.app.career.views.add_town')
]
