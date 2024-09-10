from django.db.models import BooleanField, CharField, TextField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from itdagene.core.models import BaseModel


class Question(BaseModel):
    question = CharField(max_length=100, verbose_name=_("question"))
    answer = TextField(verbose_name=_("answer"))
    is_for_companies = BooleanField(default=False, verbose_name=_("For companies"))

    def get_absolute_url(self) -> str:
        return reverse("itdagene.faq.add_question")

    def __str__(self):
        return str(self.question)
