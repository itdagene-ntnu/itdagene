from django.shortcuts import render
from itdagene.core.log.models import LogItem
from itdagene.core.decorators import superuser_required
from django.utils.translation import ugettext_lazy as _


@superuser_required()
def landing_page(request):
    return render(request, "admin/dashboard.html", {"title": _("Admin")})


@superuser_required()
def log(request, first_object=0):
    if int(first_object) > 40:
        previous = int(first_object) - 40
    else:
        previous = None
    log = (
        LogItem.objects.all()
        .select_related("user", "content_type")
        .prefetch_related("content_object")
        .order_by("timestamp")
        .reverse()[int(first_object) : int(first_object) + 40]
    )
    return render(
        request,
        "admin/log.html",
        {
            "log": log,
            "previous": previous,
            "next": int(first_object) + 41,
            "title": _("Log"),
        },
    )
