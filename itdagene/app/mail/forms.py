from django import forms
from itdagene.app.mail.models import MailMapping


class MailMappingForm(forms.ModelForm):
    class Meta:
        model = MailMapping
        fields = ('address', 'users', 'groups')