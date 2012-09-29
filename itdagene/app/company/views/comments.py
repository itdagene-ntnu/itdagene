from datetime import datetime
from django.http import Http404
from itdagene.app.company.forms import CommentForm
from itdagene.app.company.models import Comment
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

def comment(request):
    if request.method != 'POST':
        raise Http404
    comment = Comment(user=request.user,timestamp=datetime.now())
    form = CommentForm(request.POST, instance=comment)
    if form.is_valid():
        comment = form.save()
        return redirect(
            reverse('app.company.views.view', args=[comment.company.pk])
        )

@permission_required('company.change_company')
def list_comments(request):
    comments = Comment.objects.all().order_by('timestamp').reverse()[:100]
    return render(request, 'company/comments/list_all.html', {'comments': comments})