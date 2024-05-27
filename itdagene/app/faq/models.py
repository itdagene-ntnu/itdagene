from django.db import models
from itdagene.core.models import BaseModel

from django.utils.translation import gettext_lazy as _

class Question(BaseModel):
    question = models.CharField(max_length=100, verbose_name=_("question"))
    answer = models.TextField(verbose_name=_("answer"))

    def get_absolute_url(self):
        return reverse("itdagene.faq.add")

    def __str__(self):
	    return self.question
