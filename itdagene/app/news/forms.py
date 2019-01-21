from django.forms.models import ModelForm
from itdagene.app.news.models import Announcement


class AnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
        fields = ("title", "content", "image", "public")
