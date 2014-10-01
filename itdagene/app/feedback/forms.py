from django import forms
from django.forms import ChoiceField, RadioSelect, IntegerField
from itdagene.app.feedback.models import Issue, Evaluation
from django.forms.models import ModelForm
from itdagene.core.models import User

class IssueForm(ModelForm):
    class Meta:
        model = Issue
        exclude = ('is_solved', 'solved_date', 'assigned_user')

class IssueAssignForm(ModelForm):
    class Meta:
        model = Issue
        fields = ('assigned_user',)

    def __init__(self, *args, **kwargs):
        super(IssueAssignForm, self).__init__(*args, **kwargs)
        users = User.objects.filter(is_active=True, is_staff=True).order_by('first_name')
        self.fields['assigned_user'].queryset = users


class EvaluationForm (forms.ModelForm):
    class Meta:
        model = Evaluation
        exclude = ('hash',)


    def __init__(self, *args, **kwargs):
        super(EvaluationForm, self).__init__(*args, **kwargs)
#        for field in self.fields:
#            if isinstance(self.fields[field], ChoiceField):
#                self.fields[field].widget = RadioSelect()

        if self.instance.hash:
            if not self.instance.hash.company.mp and not self.instance.hash.company.partner:
                del self.fields['course_rating']
                del self.fields['course_improvement']

            if self.instance.hash.company.package_id == 6 \
            or self.instance.hash.company.package_id == 7 :
                del self.fields['internship_marathon_rating']
                del self.fields['internship_marathon_improvement']
