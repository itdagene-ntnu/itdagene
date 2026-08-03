import os

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms.models import ModelForm
from django.utils.translation import gettext_lazy as _
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
        labels = {
            "slug": _("Kortnavn i nettadressen"),
            "company": _("Bedrift"),
            "description": _("Beskrivelse"),
            "livestream_url": _("Lenke til direktesending"),
            "qa_url": _("Lenke til spørsmål og svar"),
            "chat_url": _("Lenke til chat"),
            "active": _("Aktiv"),
        }
        help_texts = {
            "slug": _(
                "Kortnavnet opprettes automatisk fra bedriftsnavnet dersom "
                "feltet står tomt."
            )
        }


class StandMapForm(ModelForm):
    MAX_UPLOAD_BYTES = 10 * 1024 * 1024
    MAX_PIXELS = 25 * 1000 * 1000
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
    ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP"}

    class Meta:
        model = StandMap
        fields = ("date", "label", "location", "background")
        labels = {
            "date": _("Dato"),
            "label": _("Navn på messedag"),
            "location": _("Sted"),
            "background": _("Bakgrunnsbilde"),
        }
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}

    def clean_background(self):
        background = self.cleaned_data["background"]
        extension = os.path.splitext(background.name)[1].lower()
        if extension not in self.ALLOWED_EXTENSIONS:
            raise ValidationError("Last opp et bilde i JPG-, PNG- eller WebP-format.")
        if background.size > self.MAX_UPLOAD_BYTES:
            raise ValidationError("Bildet må være 10 MB eller mindre.")
        try:
            image = Image.open(background)
            if image.format not in self.ALLOWED_IMAGE_FORMATS:
                raise ValidationError(
                    "Last opp et bilde i JPG-, PNG- eller WebP-format."
                )
            if image.width * image.height > self.MAX_PIXELS:
                raise ValidationError("Bildet må være 25 megapiksler eller mindre.")
            image.verify()
        except (Image.DecompressionBombError, OSError, SyntaxError):
            raise ValidationError("Last opp en gyldig bildefil.")
        finally:
            background.seek(0)
        return background


class StandPlacementForm(ModelForm):
    class Meta:
        model = StandPlacement
        fields = ("company", "stand_number", "x_percent", "y_percent")
        labels = {
            "company": _("Bedrift"),
            "stand_number": _("Standnummer"),
            "x_percent": _("X-posisjon (%)"),
            "y_percent": _("Y-posisjon (%)"),
        }
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
        companies = Company.objects.filter(active=True)
        if self.instance.company_id:
            companies = Company.objects.filter(
                Q(active=True) | Q(pk=self.instance.company_id)
            )
        self.fields["company"].queryset = companies.order_by("name", "pk")
        for field_name, field in self.fields.items():
            field.widget.attrs["data-stand-field"] = field_name
