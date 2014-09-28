from django import forms
from itdagene.core.models import User
from django.forms.widgets import PasswordInput
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from itdagene.core.profiles.models import Profile

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'mail_prefix', 'phone', 'language', 'photo', 'is_superuser', 'is_staff', 'groups', 'user_permissions')

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'mail_prefix', 'phone', 'language', 'photo', 'is_superuser', 'is_staff', 'groups', 'user_permissions')


class SimpleUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'mail_prefix', 'phone', 'language', 'photo')






class UserEditProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('type', 'position', 'year', 'phone', 'language', 'photo', 'mail_notification')


class UserEditProfileStandardForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'language', 'photo', 'mail_notification')