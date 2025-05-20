from django.urls import re_path

from itdagene.app.gallery.views import (
    add_photo,
    delete_photo,
    edit_photo,
    list_photos,
    reorder_photos,
)


urlpatterns = [
    re_path(r"^$", list_photos, name="itdagene.gallery.list_photos"),
    re_path(r"^add/$", add_photo, name="itdagene.gallery.add_photo"),
    re_path(r"^(?P<pk>\d+)/edit/$", edit_photo, name="itdagene.gallery.edit_photo"),
    re_path(
        r"^(?P<pk>\d+)/delete/$", delete_photo, name="itdagene.gallery.delete_photo"
    ),
    re_path(r"^reorder_photos", reorder_photos, name="itdagene.gallery.reorder_photos"),
]
