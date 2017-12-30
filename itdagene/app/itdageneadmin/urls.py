from django.urls import re_path

from itdagene.app.itdageneadmin.views import groups, landing_page, log, preferences

urlpatterns = [
    re_path(r'^$', landing_page, name='itdagene.app.itdageneadmin.views.landing_page'),
    re_path(r'^log$', log, name='itdagene.app.itdageneadmin.views.log'),
    re_path(r'^log/(?P<first_object>\d+)$', log, name='itdagene.app.itdageneadmin.views.log'),
    re_path(r'^groups/$', groups.list, name='itdagene.app.itdageneadmin.views.groups.list'),
    re_path(r'^groups/add$', groups.add, name='itdagene.app.itdageneadmin.views.groups.add'),
    re_path(
        r'^groups/(?P<id>\d+)/$', groups.view, name='itdagene.app.itdageneadmin.views.groups.view'
    ),
    re_path(
        r'^groups/(?P<id>\d+)/edit$', groups.edit,
        name='itdagene.app.itdageneadmin.views.groups.edit'
    ),
    re_path(
        r'^groups/(?P<id>\d+)/add/user/$', groups.add_user,
        name='itdagene.app.itdageneadmin.views.groups.add_user'
    ),
    re_path(
        r'^preferences/$', preferences.edit,
        name='itdagene.app.itdageneadmin.views.preferences.edit'
    ),
]
