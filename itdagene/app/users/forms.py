from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, ValidationError

from itdagene.core.models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "email",
            "phone",
            "linkedin",
            "language",
            "mail_notification",
            "photo",
            "year",
            "is_superuser",
            "is_staff",
            "groups",
            "user_permissions",
        )

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError(
            self.error_messages["duplicate_username"],
            code="duplicate_username",
        )


class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "linkedin",
            "language",
            "mail_notification",
            "photo",
            "year",
            "is_superuser",
            "is_staff",
            "groups",
            "user_permissions",
        )


class SimpleUserEditForm(ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "linkedin",
            "language",
            "mail_notification",
            "photo",
        )
