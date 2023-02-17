from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from itdagene.core.models import Preference


def error403(request, exception, **kwargs):
    return render(request, "static/403.html", {"title": _("Permission Denied")})


def error404(request, exception, **kwargs):
    return render(request, "static/404.html", {"title": _("Page not Found")})


def error500(request, **kwargs):
    return render(request, "static/500.html", {"title": _("Internal Server Error")})


def under_development(request, **kwargs):
    year = Preference.current_preference().year
    return render(
        request,
        "static/under_development.html",
        {"title": _("Under Development"), "year": year},
    )
