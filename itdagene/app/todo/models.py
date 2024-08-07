from django.db.models import CASCADE, BooleanField, DateTimeField, ForeignKey, TextField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from itdagene.core.models import BaseModel, User


class Todo(BaseModel):
    user = ForeignKey(
        User, on_delete=CASCADE, related_name="todos", verbose_name=_("user")
    )
    description = TextField(verbose_name=_("description"))
    deadline = DateTimeField(blank=True, null=True, verbose_name=_("deadline"))
    finished = BooleanField(verbose_name=_("finished"), default=False)

    def __str__(self) -> str:
        return str(self.description)

    def get_absolute_url(self) -> str:
        return reverse("itdagene.todo.view_todo", args=[self.pk])
