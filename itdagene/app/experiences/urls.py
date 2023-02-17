from django.urls import re_path

from itdagene.app.experiences import views

urlpatterns = [
    re_path(r"^$", views.list, name="itdagene.experiences.list"),
    re_path(r"^add$", views.add, name="itdagene.experiences.add"),
    re_path(r"^(?P<id>\d+)/$", views.view, name="itdagene.experiences.view"),
    re_path(r"^(?P<id>\d+)/edit$",
            views.edit,
            name="itdagene.experiences.edit"),
]
