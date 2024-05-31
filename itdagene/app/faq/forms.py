from django.forms.models import ModelForm

from itdagene.app.faq.models import Question


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = (
            "question",
            "answer",
        )
