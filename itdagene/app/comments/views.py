from django.contrib.auth.decorators import permission_required
from django.contrib.messages import ERROR, add_message
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from itdagene.app.comments.forms import CommentForm
from itdagene.app.mail.tasks import send_comment_email


@permission_required("comments.add_comment")
def add(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.date = timezone.now()
            instance.save()

            send_comment_email(instance)

            return redirect(instance.object.get_absolute_url())
        else:
            add_message(request, ERROR, _("Could not post comment"))
            object_ = form.instance.object
            return redirect(object_.get_absolute_url())
