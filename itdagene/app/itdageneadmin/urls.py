from django.conf.urls import url
from itdagene.app.itdageneadmin.views import landing_page, log
from itdagene.app.itdageneadmin.views import groups, preferences

urlpatterns = [
    url(r'^$', landing_page, name='itdagene.app.itdageneadmin.views.landing_page'),
    url(r'^log$', log, name='itdagene.app.itdageneadmin.views.log'),
    url(r'^log/(?P<first_object>\d+)$', log, name='itdagene.app.itdageneadmin.views.log'),

    url(r'^groups/$', groups.list, name='itdagene.app.itdageneadmin.views.groups.list'),
    url(r'^groups/add$', groups.add, name='itdagene.app.itdageneadmin.views.groups.add'),
    url(r'^groups/(?P<id>\d+)/$', groups.view, name='itdagene.app.itdageneadmin.views.groups.view'),
    url(r'^groups/(?P<id>\d+)/edit$', groups.edit, name='itdagene.app.itdageneadmin.views.groups.edit'),
    url(r'^groups/(?P<id>\d+)/add/user/$', groups.add_user, name='itdagene.app.itdageneadmin.views.groups.add_user'),

    url(r'^preferences/$', preferences.edit, name='itdagene.app.itdageneadmin.views.preferences.edit'),
]