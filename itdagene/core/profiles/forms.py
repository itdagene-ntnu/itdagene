from itdagene.core.profiles.models import Profile
from django.forms.widgets import PasswordInput
from django.forms.models import ModelForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class StandardProfileForm(ModelForm):

    class Meta:
        model = Profile
        exclude = ('user','type', 'position','year')

class StandardUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class AdminProfileForm(ModelForm):

    class Meta:
        model = Profile
        exclude = ('user',)

class ProfileSearchForm(forms.Form):
    q = forms.CharField()


class PasswordForm(forms.Form):
    old = forms.CharField(widget=PasswordInput, label=_('Old password'))
    new1 = forms.CharField(widget=PasswordInput, label=_('New password'))
    new2 = forms.CharField(widget=PasswordInput, label=_('New password again'), required=True)

class ForgotPasswordForm(forms.Form):
    email = forms.CharField(label=_('Email'))
