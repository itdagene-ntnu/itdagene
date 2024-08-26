from django.db.models import BooleanField, CharField, ImageField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from itdagene.core.models import BaseModel


class Photo(BaseModel):
    photo = ImageField(upload_to="gallery", verbose_name=_("Photo"))
    active = BooleanField(verbose_name=_("active"), default=False)

    def get_absolute_url(self) -> str:
        return reverse("itdagene.gallery.add_photo")

    def __str__(self) -> str:
        return str(self.photo.name)

    @property
    def filename(self) -> str:
        prefix = "gallery/"
        if self.photo.name.startswith(prefix):
            return self.photo.name[len(prefix) :]
        return self.photo.name
