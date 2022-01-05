from django.urls import re_path

from itdagene.app.stands import views

urlpatterns = [
    re_path(r"^stands/$", views.list, name="itdagene.stands.list"),
    re_path(r"^stands/add/$", views.add, name="itdagene.stands.add"),
    re_path(r"^stands/(?P<pk>\d+)/$", views.view, name="itdagene.stands.view"),
    re_path(r"^stands/(?P<pk>\d+)/edit/$", views.edit, name="itdagene.stands.edit"),
    re_path(
        r"^stands/(?P<pk>\d+)/delete/$",
        views.delete,
        name="itdagene.stands.delete",
    ),
]
