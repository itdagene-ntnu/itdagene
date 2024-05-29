from django.forms.models import ModelForm

from itdagene.app.gallery.models import Photo

class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = (
            "photo",
            "name",
        )
