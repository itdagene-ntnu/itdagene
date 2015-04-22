from datetime import datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.messages import *
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from itdagene.app.comments.forms import CommentForm


@permission_required('comments.add_comment')
def add(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.date = datetime.now()
            instance.save()

            return redirect(instance.object.get_absolute_url())
        else:
            print form.errors
            add_message(request, ERROR, _('Could not post comment'))
            object = form.instance.object
            return redirect(object.get_absolute_url())
