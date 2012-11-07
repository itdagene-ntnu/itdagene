from django.forms.widgets import HiddenInput
from itdagene.app.comments.models import Comment
from django.forms.models import ModelForm

class CommentForm (ModelForm):

    class Meta:
        model = Comment
        exclude = ('user', 'object','date', 'reply_to')
        widgets = {
                'object_id' : HiddenInput(),
                'content_type' : HiddenInput(),
            }