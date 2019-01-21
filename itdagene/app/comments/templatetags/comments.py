# -*- coding: utf8 -*-
from django.contrib.contenttypes.models import ContentType
from django.template import Library
from itdagene.app.comments.forms import CommentForm
from itdagene.app.comments.models import Comment

register = Library()


@register.inclusion_tag("comments/templatetags/list.html", takes_context=True)
def load_comments(context, object):
    type = ContentType.objects.get_for_model(object)
    id = object.id
    comments = (
        Comment.objects.filter(content_type=type, object_id=id)
        .order_by("-date")
        .select_related("user")
    )
    form = False
    if context["request"].user.has_perm("comments.add_comment"):
        form = CommentForm(instance=Comment(content_type=type, object_id=id))
    return {"comments": comments, "form": form}
