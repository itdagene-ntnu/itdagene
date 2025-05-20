from django.core.exceptions import ValidationError
from django.db.models import BooleanField, ImageField, Max, PositiveIntegerField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from itdagene.core.models import BaseModel


def validate_order(value):
    if value < 1:
        raise ValidationError(_("This value can not be zero and below"))


class Photo(BaseModel):
    photo = ImageField(upload_to="gallery", verbose_name=_("photo"))
    active = BooleanField(verbose_name=_("active"), default=True)
    order = PositiveIntegerField(
        default=1,
        verbose_name=_("display_order"),
        validators=[validate_order],
        unique=True,
    )

    class Meta:
        ordering = ["order"]

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

    def delete(self, using=None, keep_parents=False):
        """
        Actually delete the image file when model is deleted.
        Django recommends doing periodical cleanup instead since this
        solution may lead to orphaned files if a runtime error happens.
        """
        storage = self.photo.storage

        if storage.exists(self.photo.name):
            storage.delete(self.photo.name)

        super().delete()

    def clean(self):
        super().clean()

        if self.pk is None:
            max_order = Photo.objects.aggregate(Max("order"))["order__max"] or 0
            self.order = max_order + 1

    def save(self, **kwargs):
        super().full_clean()
        super().save(**kwargs)
