from datetime import datetime
from django.conf import settings
from django.contrib.auth.decorators import permission_required, login_required
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from itdagene.app.comments.forms import CommentForm
from django.http import HttpResponsePermanentRedirect
from itdagene.app.comments.models import Comment
from django.shortcuts import render


@permission_required('comments.add_comment')
def add(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.date = datetime.now()
            instance.save()

            send_mail('[itDAGENE] Someone commented on a ' + str(instance.content_type),
                      'Hi\n\nSomeone commented on a '+ str(instance.content_type) + ' that you created: ' + str(instance.object),
                      settings.FROM_ADDRESS,(instance.object.creator.email,))

            return HttpResponsePermanentRedirect(instance.object.get_absolute_url())
        else:
            print form.errors
            request.session['message'] = {'class': 'danger', 'value': _('Could not post comment, error') + ': ' + ': '.join([k + ': ' + v for k, v in form.errors])}
            return all(request)


@permission_required('comments.add_comment')
def all(request):
    comments = Comment.objects.filter(reply_to=None).select_related('replies')
    return render(request,'comments/list.html',
                             {'comments': comments})