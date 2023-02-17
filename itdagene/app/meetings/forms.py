from django import forms
from django.forms.models import ModelForm
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from itdagene.app.meetings.models import Meeting, Penalty, ReplyMeeting
from itdagene.core.models import Preference, User


class MeetingForm(ModelForm):
    invites = forms.MultipleChoiceField(label=_("Invite"), required=False)
    invite_current_board = forms.BooleanField(label=_("Invite current board"),
                                              required=False)

    class Meta:
        model = Meeting
        exclude = ("is_board_meeting", "preference")

    def __init__(self, *args, **kwargs):
        super(MeetingForm, self).__init__(*args, **kwargs)
        pref = Preference.current_preference()
        users = User.objects.filter(is_active=True,
                                    is_staff=True,
                                    year=pref.year)

        self.fields["referee"].queryset = users
        self.fields["invites"].choices = [(user.pk, user.get_full_name())
                                          for user in users]

    def save(self, commit=True):
        pref = Preference.current_preference()
        meeting = super(MeetingForm, self).save(commit=commit)

        for i in self.cleaned_data["invites"]:
            user = get_object_or_404(User,
                                     id=i,
                                     is_staff=True,
                                     is_active=True,
                                     year=pref.year)
            ReplyMeeting.objects.get_or_create(meeting=meeting,
                                               user_id=user.id)

        if self.cleaned_data["invite_current_board"]:
            for user in User.objects.filter(year=pref.year,
                                            is_staff=True,
                                            is_active=True):
                ReplyMeeting.objects.get_or_create(meeting=meeting,
                                                   user_id=user.id)

        return meeting


class AbstractForm(ModelForm):

    class Meta:
        model = Meeting
        exclude = ("date", "start_time", "end_time", "is_board_member")


class PenaltyForm(ModelForm):

    class Meta:
        model = Penalty
        exclude = ("meeting", )

    def __init__(self, *args, **kwargs):
        super(PenaltyForm, self).__init__(*args, **kwargs)
        pref = Preference.current_preference()
        users = User.objects.filter(is_active=True,
                                    is_staff=True,
                                    year=pref.year)
        self.fields["user"].queryset = users
