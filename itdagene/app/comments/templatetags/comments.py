from django.contrib.contenttypes.models import ContentType
from django.template.base import Library
from itdagene.app.comments.forms import CommentForm
from itdagene.app.comments.models import Comment

register = Library()

@register.inclusion_tag('comments/templatetags/list.html')
def load_comments(object):
    type = ContentType.objects.get_for_model(object)
    id = object.id
    comments = Comment.objects.filter(content_type=type, object_id=id)
    form = CommentForm(instance=Comment(content_type=type, object_id=id))
    return {'comments': comments, 'form': form}
