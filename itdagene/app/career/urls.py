from django.conf.urls import url, patterns


urlpatterns = patterns('itdagene.app.career.views',
    url(r'^joblistings/$', 'list'),
    url(r'^joblistings/add/$', 'add'),
    url(r'^joblistings/(?P<pk>\d+)/$', 'view'),
    url(r'^joblistings/(?P<pk>\d+)/edit/$', 'edit'),
    url(r'^joblistings/(?P<pk>\d+)/delete/$', 'delete'),
    url(r'^joblistings/add_town/$', 'add_town')
)

