from django.forms.models import ModelForm

from itdagene.app.stands.models import DigitalStand


class DigitalStandForm(ModelForm):
    class Meta:
        model = DigitalStand
        fields = (
            "slug",
            "company",
            "description",
            "livestream",
            "qa",
            "chat",
            "active",
        )
