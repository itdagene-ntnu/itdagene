from django.db.models import CharField, ImageField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from itdagene.core.models import BaseModel


class Photo(BaseModel):
    name = CharField(max_length=100, unique=True, verbose_name=_("Photo name"))
    photo = ImageField(upload_to="gallery", verbose_name=_("Photo"))

    def get_absolute_url(self) -> str:
        return reverse("itdagene.gallery.add_photo")

    def __str__(self) -> str:
        return str(self.name)
