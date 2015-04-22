from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'itdagene.app.users.views.user_list', name='list'),
    url(r'^create/$', 'itdagene.app.users.views.user_create', name='create'),
    url(r'^(?P<pk>\d+)/$', 'itdagene.app.users.views.user_detail', name='detail'),
    url(r'^(?P<pk>\d+)/welcome_email/$', 'itdagene.app.users.views.send_welcome_email'),
    url(r'^(?P<pk>\d+)/vcard/$', 'itdagene.app.users.views.vcard'),
    url(r'^(?P<pk>\d+)/edit/$', 'itdagene.app.users.views.user_edit', name='edit'),
    url(r'^(?P<pk>\d+)/edit/password/$', 'itdagene.app.users.views.user_edit_password',
        name='edit_password'),
    url(r'^(?P<pk>\d+)/delete/$', 'itdagene.app.users.views.user_delete', name='delete'),
]
