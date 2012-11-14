from django import forms
from django.forms.forms import Form
from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _
from itdagene.app.meetings.models import Meeting, ReplyMeeting
from django.contrib.auth.models import User


class MeetingForm(ModelForm):
    invites = forms.MultipleChoiceField(label=_('invite'))
    class Meta:
        model = Meeting
        exclude = ('is_board_meeting',)

    def __init__(self, *args, **kwargs):
        super(MeetingForm, self).__init__(*args, **kwargs)
        users = User.objects.filter(is_active=True, profile__type='b').order_by('first_name')
        self.fields['referee'].choices = [(user.pk, user.get_full_name()) for user in users]
        self.fields['invites'].choices = [(user.pk, user.get_full_name()) for user in users]
        self.fields['invites'].widget.attrs['class'] = 'chosen'

    def save(self, commit=True):
        meeting = super(MeetingForm, self).save(commit=commit)

        for i in self.cleaned_data['invites']:
            ReplyMeeting.objects.get_or_create(meeting=meeting, user_id=i)

        return meeting

class AbstractForm(ModelForm):
    class Meta:
        model = Meeting
        exclude = ('date', 'start_time', 'end_time', 'is_board_member')

class SearchForm(Form):
    query = forms.CharField()