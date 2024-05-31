from django.db import models
from django.utils.translation import gettext_lazy as _

from itdagene.core.models import BaseModel


class Photo(BaseModel):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Photo name"))
    photo = models.ImageField(upload_to="gallery", verbose_name=_("Photo"))

    def get_absolute_url(self):
        return reverse("itdagene.gallery.add_photo")

    def __str__(self):
        return self.name
