from django.contrib.auth.decorators import permission_required
from django.contrib.messages import SUCCESS, add_message
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from itdagene.app.experiences.forms import ExperienceForm
from itdagene.app.experiences.models import Experience
from itdagene.core.decorators import staff_required
from itdagene.core.models import Preference


@staff_required()
def list(request: HttpRequest) -> HttpResponse:
    experience_lists = []
    for pref in Preference.objects.all().order_by("-year"):
        experience_lists.append(
            (
                pref.year,
                Experience.objects.filter(year__year=pref.year).order_by("position"),
            )
        )
    return render(
        request,
        "experiences/list.html",
        {"experience_lists": experience_lists, "title": _("Experiences")},
    )


@staff_required()
def view(request: HttpRequest, id) -> HttpResponse:
    experience = get_object_or_404(Experience, pk=id)
    return render(
        request,
        "experiences/view.html",
        {
            "experience": experience,
            "title": _("Experience"),
            "description": f"{experience} {experience.year.year}",
        },
    )


@permission_required("experiences.add_experience")
def add(request: HttpRequest) -> HttpResponse:
    form = ExperienceForm()
    if request.method == "POST":
        form = ExperienceForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.year = Preference.get_preference_by_year(request.user.year)
            data.save()
            add_message(request, SUCCESS, _("Experience added."))
            return redirect(reverse("itdagene.experiences.view", args=[data.pk]))
    return render(
        request, "experiences/form.html", {"form": form, "title": _("Add Experience")}
    )


@permission_required("experiences.change_experience")
def edit(request: HttpRequest, id) -> HttpResponse:
    es = get_object_or_404(Experience, pk=id)
    form = ExperienceForm(instance=es)
    if request.method == "POST":
        form = ExperienceForm(request.POST, instance=es)
        if form.is_valid():
            data = form.save()
            return redirect(reverse("itdagene.experiences.view", args=[data.pk]))
    return render(
        request,
        "experiences/form.html",
        {
            "form": form,
            "experience": es,
            "title": _("Edit Experience"),
            "description": f"{es} {es.year.year}",
        },
    )
