from django.forms.models import ModelForm

from itdagene.app.stands.models import DigitalStand


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
