from django.contrib.auth.decorators import permission_required
from django.contrib.messages import ERROR, add_message
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from itdagene.app.comments.forms import CommentForm
from itdagene.app.mail.tasks import send_comment_email


@permission_required("comments.add_comment")
def add(request):
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
            object = form.instance.object
            return redirect(object.get_absolute_url())
