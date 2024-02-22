from django.urls import re_path

from itdagene.app.itdageneadmin.views import (
    companies_reset,
    groups,
    landing_page,
    log,
    preferences,
)


urlpatterns = [
    re_path(r"^$", landing_page, name="itdagene.itdageneadmin.landing_page"),
    re_path(r"^log$", log, name="itdagene.itdageneadmin.log"),
    re_path(r"^log/(?P<first_object>\d+)$", log, name="itdagene.itdageneadmin.log"),
    re_path(r"^groups/$", groups.list, name="itdagene.itdageneadmin.groups.list"),
    re_path(r"^groups/add$", groups.add, name="itdagene.itdageneadmin.groups.add"),
    re_path(
        r"^groups/(?P<id>\d+)/$", groups.view, name="itdagene.itdageneadmin.groups.view"
    ),
    re_path(
        r"^groups/(?P<id>\d+)/edit$",
        groups.edit,
        name="itdagene.itdageneadmin.groups.edit",
    ),
    re_path(
        r"^groups/(?P<id>\d+)/add/user/$",
        groups.add_user,
        name="itdagene.itdageneadmin.groups.add_user",
    ),
    re_path(
        r"^preferences/$",
        preferences.edit,
        name="itdagene.itdageneadmin.preferences.edit",
    ),
    re_path(
        r"^companies_reset/$",
        companies_reset,
        name="itdagene.itdageneadmin.companies_reset",
    ),
]
