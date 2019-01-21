from django.urls import re_path
from itdagene.app.career import views

urlpatterns = [
    re_path(r"^joblistings/$", views.list, name="itdagene.career.list"),
    re_path(r"^joblistings/add/$", views.add, name="itdagene.career.add"),
    re_path(r"^joblistings/(?P<pk>\d+)/$", views.view, name="itdagene.career.view"),
    re_path(
        r"^joblistings/(?P<pk>\d+)/edit/$", views.edit, name="itdagene.career.edit"
    ),
    re_path(
        r"^joblistings/(?P<pk>\d+)/delete/$",
        views.delete,
        name="itdagene.career.delete",
    ),
    re_path(
        r"^joblistings/add_town/$", views.add_town, name="itdagene.career.add_town"
    ),
]
