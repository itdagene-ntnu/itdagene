from django.template.base import Library
from itdagene.app.company.forms import CommentForm
from itdagene.app.company.models import Comment

register = Library()

@register.inclusion_tag('company/comments/list.html')
def comments(company):
    comments = Comment.objects.filter(company=company).order_by('timestamp').reverse()
    return {'comments': comments}

@register.inclusion_tag('company/comments/form.html')
def comment_form(company):
    form = CommentForm(instance=Comment(company=company))
    return {'form': form}
