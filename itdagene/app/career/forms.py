from django.forms.models import ModelForm

from itdagene.app.career.models import Joblisting, Town


class JoblistingForm(ModelForm):
    class Meta:
        model = Joblisting
        fields = (
            "title",
            "type",
            "company",
            "description",
            "contact",
            "deadline",
            "from_grade",
            "to_grade",
            "url",
            "towns",
            "video_url",
            "is_summerjob_marathon",
            "image",
            "frontpage",
            "hide_contactinfo",
            "is_displayed",
        )


class JoblistingTownForm(ModelForm):
    class Meta:
        model = Town
        fields = ("name",)
