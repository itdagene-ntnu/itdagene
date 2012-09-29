from django import forms
from django.forms import ChoiceField, RadioSelect, IntegerField
from itdagene.app.feedback.models import Issue, Evaluation
from django.forms.models import ModelForm
from django.contrib.auth.models import User

class IssueForm(ModelForm):
    class Meta:
        model = Issue
        exclude = ('is_solved', 'solved_date', 'deadline','assigned_user')

class IssueAssignForm(ModelForm):
    class Meta:
        model = Issue
        fields = ('assigned_user',)

    def __init__(self, *args, **kwargs):
        super(IssueAssignForm, self).__init__(*args, **kwargs)
        users = User.objects.filter(is_active=True, profile__type='b').order_by('first_name')
        self.fields['assigned_user'].choices = [(user.pk, user.get_full_name()) for user in users]


class EvaluationForm (forms.ModelForm):
    class Meta:
        model = Evaluation
        exclude = ('hash',)


    def __init__(self, *args, **kwargs):
        super(EvaluationForm, self).__init__(*args, **kwargs)
#        for field in self.fields:
#            if isinstance(self.fields[field], ChoiceField):
#                self.fields[field].widget = RadioSelect()

        if self.instance.pk:
            if not self.instance.company.mp and not self.instance.company.partner:
                del self.fields['course_rating']
                del self.fields['course_improvement']
