from django.conf.urls import patterns, url

urlpatterns = patterns('itdagene.app.admin.views',
    url(r'^$', 'landing_page', name='admin' ),
    (r'^log$', 'log' ),
    (r'^log/(?P<first_object>\d+)$', 'log' ),
)

urlpatterns += patterns('itdagene.app.admin.views.groups',
    (r'^groups/$', 'list' ),
    (r'^groups/add$', 'add' ),
    (r'^groups/(?P<id>\d+)/$', 'view' ),
    (r'^groups/(?P<id>\d+)/edit$', 'edit' ),
    (r'^groups/(?P<id>\d+)/add/user/$', 'add_user' ),
)

urlpatterns += patterns('itdagene.app.admin.views.preferences',
    (r'^preferences/$', 'edit' ),
)
