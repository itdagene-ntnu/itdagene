from django import forms
from itdagene.core.models import User
from django.forms.widgets import PasswordInput
from django.utils.translation import ugettext_lazy as _

from itdagene.core.profiles.models import Profile


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='Passord', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Bekreft passord', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                'De to oppgitte passordene er ikke like',
                'password_mismatch'
            )

        return password2

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class UserEditPasswordForm(forms.Form):
    old = forms.CharField(widget=PasswordInput, label=_('Old password'))
    new1 = forms.CharField(widget=PasswordInput, label=_('New password'))
    new2 = forms.CharField(widget=PasswordInput, label=_('New password again'), required=True)


class UserEditProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('type', 'position', 'year', 'phone', 'language', 'photo', 'mail_notification')


class UserEditProfileStandardForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'language', 'photo', 'mail_notification')