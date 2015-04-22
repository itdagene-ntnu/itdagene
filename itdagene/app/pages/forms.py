from django.forms.models import ModelForm

from itdagene.app.pages.models import Page


class PageForm(ModelForm):
    class Meta:
        model = Page
