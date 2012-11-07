from django import forms
from django.forms.forms import Form
from django.forms.models import ModelForm
from itdagene.app.meetings.models import Meeting
from django.contrib.auth.models import User

class MeetingForm(ModelForm):
    class Meta:
        model = Meeting

    def __init__(self, *args, **kwargs):
        super(MeetingForm, self).__init__(*args, **kwargs)
        users = User.objects.filter(is_active=True, profile__type='b').order_by('first_name')
        self.fields['referee'].choices = [(user.pk, user.get_full_name()) for user in users]

class AbstractForm(ModelForm):
    class Meta:
        model = Meeting
        exclude = ('date', 'start_time', 'end_time', 'is_board_member')

class SearchForm(Form):
    query = forms.CharField()