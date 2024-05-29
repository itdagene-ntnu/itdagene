from django.urls import re_path

from itdagene.app.gallery.views import list_photos, add_photo, delete_photo

urlpatterns = [
    re_path(r"^$", list_photos, name="itdagene.gallery.list_photos"),
    re_path(r"^add/$", add_photo, name="itdagene.gallery.add_photo"),
    re_path(r"^(?P<pk>\d+)/delete/$", delete_photo, name="itdagene.gallery.delete_photo"),
]