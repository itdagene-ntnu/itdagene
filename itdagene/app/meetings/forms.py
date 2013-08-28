from django import forms
from django.forms.forms import Form
from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _
from itdagene.app.meetings.models import Meeting, ReplyMeeting
from django.contrib.auth.models import User
from itdagene.core import Preference
from itdagene.core.profiles.models import Profile


class MeetingForm(ModelForm):
    invites = forms.MultipleChoiceField(label=_('invite'), required=False)
    invite_current_board = forms.BooleanField(label=_('Invite current board'), required=False)

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
        pref = Preference.current_preference()
        meeting = super(MeetingForm, self).save(commit=commit)

        for i in self.cleaned_data['invites']:
            ReplyMeeting.objects.get_or_create(meeting=meeting, user_id=i)

        if self.cleaned_data['invite_current_board']:
            for profile in Profile.objects.filter(year=pref.year, type='b'):
                ReplyMeeting.objects.get_or_create(meeting=meeting, user_id=profile.user_id)

        return meeting

class AbstractForm(ModelForm):
    class Meta:
        model = Meeting
        exclude = ('date', 'start_time', 'end_time', 'is_board_member')

class SearchForm(Form):
    query = forms.CharField()