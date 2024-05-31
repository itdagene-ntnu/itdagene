from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from itdagene.core.models import BaseModel


class Question(BaseModel):
    question = models.CharField(max_length=100, verbose_name=_("question"))
    answer = models.TextField(verbose_name=_("answer"))

    def get_absolute_url(self):
        return reverse("itdagene.faq.add_question")

    def __str__(self):
        return self.question
