from itdagene.app.pages.models import Page
from django.forms.models import ModelForm


class PageForm(ModelForm):
    class Meta:
        model = Page
