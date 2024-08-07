from django.db.models import CharField, TextField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from itdagene.core.models import BaseModel


class Question(BaseModel):
    question = CharField(max_length=100, verbose_name=_("question"))
    answer = TextField(verbose_name=_("answer"))

    def get_absolute_url(self) -> str:
        return reverse("itdagene.faq.add_question")

    def __str__(self):
        return str(self.question)
