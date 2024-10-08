from django.forms import Textarea
from django.forms.models import ModelForm
from django.forms.widgets import HiddenInput

from itdagene.app.comments.models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ("user", "object", "date", "reply_to")
        widgets = {
            "object_id": HiddenInput(),
            "content_type": HiddenInput(),
            "comment": Textarea(attrs={"rows": 3}),
        }
