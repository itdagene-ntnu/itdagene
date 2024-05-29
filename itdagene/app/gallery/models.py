from django.db import models
from itdagene.core.models import BaseModel

from django.utils.translation import gettext_lazy as _

class Photo(BaseModel):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Photo name"))
    photo = models.ImageField(upload_to="gallery")

    def get_absolute_url(self):
        return reverse("itdagene.gallery.add_photo")

    def __str__(self):
	    return self.name