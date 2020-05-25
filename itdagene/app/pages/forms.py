from django.forms.models import ModelForm
from itdagene.app.pages.models import Page


class PageForm(ModelForm):
    class Meta:
        model = Page
        fields = (
            "title",
            "slug",
            "content",
            "ingress",
            "language",
            "active",
            "need_auth",
            "menu",
            "is_infopage",
        )
