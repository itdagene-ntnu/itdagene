from django.conf.urls import url

urlpatterns = [
    url(r'^joblistings/$', 'itdagene.app.career.views.list'),
    url(r'^joblistings/add/$', 'itdagene.app.career.views.add'),
    url(r'^joblistings/(?P<pk>\d+)/$', 'itdagene.app.career.views.view'),
    url(r'^joblistings/(?P<pk>\d+)/edit/$', 'itdagene.app.career.views.edit'),
    url(r'^joblistings/(?P<pk>\d+)/delete/$', 'itdagene.app.career.views.delete'),
    url(r'^joblistings/add_town/$', 'itdagene.app.career.views.add_town')
]
