from django.contrib.messages import SUCCESS, add_message
from django.shortcuts import redirect, render, reverse
from django.utils.translation import ugettext_lazy as _

from itdagene.app.company import COMPANY_STATUS_NOT_CONTACTED
from itdagene.app.company.models import Company
from itdagene.core.decorators import superuser_required
from itdagene.core.log.models import LogItem


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


@superuser_required()
def companies_reset(request):

    if request.method == "POST":
        Company.objects.all().update(
            status=COMPANY_STATUS_NOT_CONTACTED,
            contact=None,
            package=None,
        )
        Company.waiting_for_package.through.objects.all().delete()

        add_message(request, SUCCESS, _("Companies reset"))
        return redirect(reverse("itdagene.itdageneadmin.landing_page"))

    return render(
        request, "admin/companies_reset.html", {"title": _("Reset companies")}
    )
