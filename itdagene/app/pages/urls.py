from django.urls import re_path
from itdagene.app.pages.views import add, admin, edit, view_page

urlpatterns = [
    re_path(r"^pages/$", admin, name="itdagene.pages.admin"),
    re_path(r"^pages/add/$", add, name="itdagene.pages.add"),
    re_path(r"^$", view_page, name="itdagene.pages.view_page"),
    re_path(r"^(?P<slug>[-_\w]+)/$", view_page, name="itdagene.pages.view_page"),
    re_path(r"^(?P<slug>[-_\w]+)/edit/$", edit, name="itdagene.pages.edit"),
    re_path(
        r"^(?P<lang_code>[a-z][a-z])/(?P<slug>[-_\w]+)/$",
        view_page,
        name="itdagene.pages.view_page",
    ),
    re_path(
        r"^(?P<lang_code>[a-z][a-z])/(?P<slug>[-_\w]+)/edit/$",
        edit,
        name="itdagene.pages.edit",
    ),
]
