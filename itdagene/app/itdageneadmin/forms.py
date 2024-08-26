from django.contrib.auth.models import Group
from django.forms import CharField, IntegerField
from django.forms.forms import Form
from django.forms.models import ModelForm

from itdagene.core.models import Preference, User


class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = (
            "username",
            "password",
            "user_permissions",
            "last_login",
            "date_joined",
        )


class RegisterUserForm(Form):
    username = CharField(max_length=8)
    first_name = CharField()
    last_name = CharField()
    phone = IntegerField()


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ("name", "permissions")


class AddUserToGroupForm(Form):
    username = CharField()


class PreferenceForm(ModelForm):
    class Meta:
        model = Preference
        exclude = ("active",)
