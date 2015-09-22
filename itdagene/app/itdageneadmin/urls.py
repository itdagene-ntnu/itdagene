from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'itdagene.app.itdageneadmin.views.landing_page', name='admin'),
    url(r'^log$', 'itdagene.app.itdageneadmin.views.log'),
    url(r'^log/(?P<first_object>\d+)$', 'itdagene.app.itdageneadmin.views.log'),

    url(r'^groups/$', 'itdagene.app.itdageneadmin.views.groups.list'),
    url(r'^groups/add$', 'itdagene.app.itdageneadmin.views.groups.add'),
    url(r'^groups/(?P<id>\d+)/$', 'itdagene.app.itdageneadmin.views.groups.view'),
    url(r'^groups/(?P<id>\d+)/edit$', 'itdagene.app.itdageneadmin.views.groups.edit'),
    url(r'^groups/(?P<id>\d+)/add/user/$', 'itdagene.app.itdageneadmin.views.groups.add_user'),

    url(r'^preferences/$', 'itdagene.app.itdageneadmin.views.preferences.edit'),
]
