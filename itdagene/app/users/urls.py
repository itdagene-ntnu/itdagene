from django.urls import re_path

from itdagene.app.company.views.company_contacts import vcard
from itdagene.app.users.views import (
    send_welcome_email, user_create, user_delete, user_detail, user_edit, user_edit_password,
    user_list
)

urlpatterns = [
    re_path(r'^$', user_list, name='itdagene.app.users.views.user_list'),
    re_path(r'^create/$', user_create, name='itdagene.app.users.views.user_create'),
    re_path(r'^(?P<pk>\d+)/$', user_detail, name='itdagene.app.users.views.user_detail'),
    re_path(
        r'^(?P<pk>\d+)/welcome_email/$', send_welcome_email,
        name='itdagene.app.users.views.send_welcome_email'
    ),
    re_path(r'^(?P<pk>\d+)/vcard/$', vcard, name='itdagene.app.users.views.vcard'),
    re_path(r'^(?P<pk>\d+)/edit/$', user_edit, name='itdagene.app.users.views.user_edit'),
    re_path(
        r'^(?P<pk>\d+)/edit/password/$', user_edit_password,
        name='itdagene.app.users.views.user_edit_password'
    ),
    re_path(r'^(?P<pk>\d+)/delete/$', user_delete, name='itdagene.app.users.views.user_delete'),
]
