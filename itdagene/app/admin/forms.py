from django.contrib.auth.models import User, Group
from django.forms.forms import Form
from django.forms.models import ModelForm
from itdagene.core.models import Preference
from django import forms

class UserForm (ModelForm):
    class Meta:
        model = User
        exclude = ('username', 'password', 'user_permissions', 'last_login', 'date_joined')


class RegisterUserForm(forms.Form):
    username = forms.CharField(max_length=8)
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone = forms.IntegerField()

class GroupForm (ModelForm):
    class Meta:
        model = Group
        fields = ('name',)

class AddUserToGroupForm(Form):
    username = forms.CharField()

class PreferenceForm (ModelForm):
    class Meta:
        model = Preference

class PermissionForm (ModelForm):
    class Meta:
        model = Preference
        
    create = forms.BooleanField()
    edit = forms.BooleanField()
    view = forms.BooleanField()
    delete = forms.BooleanField()