from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'itdagene.app.admin.views.landing_page', name='admin'),
    url(r'^log$', 'itdagene.app.admin.views.log'),
    url(r'^log/(?P<first_object>\d+)$', 'itdagene.app.admin.views.log'),

    url(r'^groups/$', 'itdagene.app.admin.views.groups.list'),
    url(r'^groups/add$', 'itdagene.app.admin.views.groups.add'),
    url(r'^groups/(?P<id>\d+)/$', 'itdagene.app.admin.views.groups.view'),
    url(r'^groups/(?P<id>\d+)/edit$', 'itdagene.app.admin.views.groups.edit'),
    url(r'^groups/(?P<id>\d+)/add/user/$', 'itdagene.app.admin.views.groups.add_user'),

    url(r'^preferences/$', 'itdagene.app.admin.views.preferences.edit'),
]
