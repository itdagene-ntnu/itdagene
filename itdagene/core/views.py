from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from itdagene.core.models import Preference


def error403(request: HttpRequest, exception: Any, **kwargs) -> HttpResponse:
    return render(request, "static/403.html", {"title": _("Permission Denied")})


def error404(request: HttpRequest, exception: Any, **kwargs) -> HttpResponse:
    return render(request, "static/404.html", {"title": _("Page not Found")})


def error500(request: HttpRequest, **kwargs) -> HttpResponse:
    return render(request, "static/500.html", {"title": _("Internal Server Error")})


def under_development(request: HttpRequest, **kwargs) -> HttpResponse:
    year = Preference.current_preference().year
    return render(
        request,
        "static/under_development.html",
        {"title": _("Under Development"), "year": year},
    )
