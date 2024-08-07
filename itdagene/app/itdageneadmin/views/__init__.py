from django.contrib.messages import SUCCESS, add_message
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, reverse
from django.utils.translation import gettext_lazy as _

from itdagene.app.company import COMPANY_STATUS_NOT_CONTACTED
from itdagene.app.company.models import Company
from itdagene.core.decorators import superuser_required
from itdagene.core.log.models import LogItem


@superuser_required()
def landing_page(request: HttpRequest) -> HttpResponse:
    return render(request, "admin/dashboard.html", {"title": _("Admin")})


@superuser_required()
def log(request: HttpRequest, first_object=0):
    first_object = int(first_object)
    previous = first_object - 40 if first_object > 40 else None
    log_ = (
        LogItem.objects.all()
        .select_related("user", "content_type")
        .prefetch_related("content_object")
        .order_by("timestamp")
        .reverse()[first_object : first_object + 40]
    )
    return render(
        request,
        "admin/log.html",
        {
            "log": log_,
            "previous": previous,
            "next": first_object + 41,
            "title": _("Log"),
        },
    )


@superuser_required()
def companies_reset(request: HttpRequest) -> HttpResponse:
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
