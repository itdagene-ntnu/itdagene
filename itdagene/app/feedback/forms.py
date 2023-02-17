from django import forms
from django.forms.models import ModelForm

from itdagene.app.feedback.models import Evaluation, Issue
from itdagene.core.models import User


class IssueForm(ModelForm):
    class Meta:
        model = Issue
        exclude = ("is_solved", "solved_date", "assigned_user")


class IssueAssignForm(ModelForm):
    class Meta:
        model = Issue
        fields = ("assigned_user",)

    def __init__(self, *args, **kwargs):
        super(IssueAssignForm, self).__init__(*args, **kwargs)
        users = User.objects.filter(is_active=True, is_staff=True).order_by(
            "first_name"
        )
        self.fields["assigned_user"].queryset = users


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        exclude = ("hash", "company", "has_answers", "preference")

    def save(self, commit=True, *args, **kwargs):
        self.instance.has_answers = True
        super(EvaluationForm, self).save(*args, **kwargs)
