import os

from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from PIL import Image

from itdagene.app.company.models import Company
from itdagene.app.stands.models import DigitalStand, StandMap, StandPlacement


class DigitalStandForm(ModelForm):
    class Meta:
        model = DigitalStand
        fields = (
            "slug",
            "company",
            "description",
            "livestream_url",
            "qa_url",
            "chat_url",
            "active",
        )


class StandMapForm(ModelForm):
    MAX_UPLOAD_BYTES = 10 * 1024 * 1024
    MAX_PIXELS = 25 * 1000 * 1000
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
    ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP"}

    class Meta:
        model = StandMap
        fields = ("date", "label", "location", "background")
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}

    def clean_background(self):
        background = self.cleaned_data["background"]
        extension = os.path.splitext(background.name)[1].lower()
        if extension not in self.ALLOWED_EXTENSIONS:
            raise ValidationError("Upload a JPG, PNG, or WebP raster image.")
        if background.size > self.MAX_UPLOAD_BYTES:
            raise ValidationError("The image must be 10 MB or smaller.")
        try:
            image = Image.open(background)
            if image.format not in self.ALLOWED_IMAGE_FORMATS:
                raise ValidationError("Upload a JPG, PNG, or WebP raster image.")
            if image.width * image.height > self.MAX_PIXELS:
                raise ValidationError("The image must be 25 megapixels or smaller.")
            image.verify()
        except (Image.DecompressionBombError, OSError, SyntaxError):
            raise ValidationError("Upload a valid raster image.")
        finally:
            background.seek(0)
        return background


class StandPlacementForm(ModelForm):
    class Meta:
        model = StandPlacement
        fields = ("company", "stand_number", "x_percent", "y_percent")
        widgets = {
            "x_percent": forms.NumberInput(
                attrs={"min": 0, "max": 100, "step": "0.01"}
            ),
            "y_percent": forms.NumberInput(
                attrs={"min": 0, "max": 100, "step": "0.01"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(StandPlacementForm, self).__init__(*args, **kwargs)
        self.fields["company"].queryset = Company.get_signed_with_packages()
