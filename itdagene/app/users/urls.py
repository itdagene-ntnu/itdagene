from django.conf.urls import url

from itdagene.app.company.views.company_contacts import vcard
from itdagene.app.users.views import (
    send_welcome_email, user_create, user_delete, user_detail, user_edit, user_edit_password,
    user_list
)

urlpatterns = [
    url(r'^$', user_list, name='itdagene.app.users.views.user_list'),
    url(r'^create/$', user_create, name='itdagene.app.users.views.user_create'),
    url(r'^(?P<pk>\d+)/$', user_detail, name='itdagene.app.users.views.user_detail'),
    url(
        r'^(?P<pk>\d+)/welcome_email/$', send_welcome_email,
        name='itdagene.app.users.views.send_welcome_email'
    ),
    url(r'^(?P<pk>\d+)/vcard/$', vcard, name='itdagene.app.users.views.vcard'),
    url(r'^(?P<pk>\d+)/edit/$', user_edit, name='itdagene.app.users.views.user_edit'),
    url(
        r'^(?P<pk>\d+)/edit/password/$', user_edit_password,
        name='itdagene.app.users.views.user_edit_password'
    ),
    url(r'^(?P<pk>\d+)/delete/$', user_delete, name='itdagene.app.users.views.user_delete'),
]
