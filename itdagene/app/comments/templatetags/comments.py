from typing import Union

from django.contrib.contenttypes.models import ContentType
from django.template import Library

from itdagene.app.comments.forms import CommentForm
from itdagene.app.comments.models import Comment


register = Library()


@register.inclusion_tag("comments/templatetags/list.html", takes_context=True)
def load_comments(context, object) -> dict:
    type_ = ContentType.objects.get_for_model(object)
    id_ = object.id
    comments = (
        Comment.objects.filter(content_type=type_, object_id=id_)
        .order_by("-date")
        .select_related("user")
    )
    form: Union[bool, CommentForm] = False
    if context["request"].user.has_perm("comments.add_comment"):
        form = CommentForm(instance=Comment(content_type=type_, object_id=id_))
    return {"comments": comments, "form": form}
