from django import forms
from django.contrib.auth.forms import UserCreationForm

from itdagene.core.models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name',
                  'last_name', 'email', 'phone', 'language',
                  'mail_notification', 'photo', 'year', 'is_superuser',
                  'is_staff', 'groups', 'user_permissions')

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'],
                                    code='duplicate_username', )


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'language',
                  'mail_notification', 'photo', 'year', 'is_superuser',
                  'is_staff', 'groups', 'user_permissions')


class SimpleUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'language',
                  'mail_notification', 'photo')
