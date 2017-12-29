from django.conf.urls import url

from itdagene.app.career import views

urlpatterns = [
    url(r'^joblistings/$', views.list, name='itdagene.app.career.views.list'),
    url(r'^joblistings/add/$', views.add, name='itdagene.app.career.views.add'),
    url(r'^joblistings/(?P<pk>\d+)/$', views.view),
    url(r'^joblistings/(?P<pk>\d+)/edit/$', views.edit),
    url(r'^joblistings/(?P<pk>\d+)/delete/$', views.delete),
    url(r'^joblistings/add_town/$', views.add_town, name='itdagene.app.career.views.add_town')
]
