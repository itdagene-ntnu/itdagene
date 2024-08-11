from django.contrib.messages import SUCCESS, add_message
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from itdagene.app.feedback.forms import EvaluationForm
from itdagene.app.feedback.models import Evaluation
from itdagene.core.decorators import staff_required
from itdagene.core.models import Preference


EN = [1065]


def handle_evaluation(request: HttpRequest, hash: str) -> HttpResponse:
    evaluation = get_object_or_404(Evaluation, hash=hash)
    form = EvaluationForm(instance=evaluation)
    if request.method == "POST":
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            add_message(
                request,
                SUCCESS,
                _(
                    "Thank you for your interest I itDAGENE . We "
                    "hope you will come back next next year."
                ),
            )
            return redirect(reverse("itdagene.frontpage.frontpage"))
    return render(request, "feedback/evaluations/handle_evaluate.html", {"form": form})


@staff_required()
def report(request: HttpRequest, year=None) -> HttpResponse:
    preferences = (
        Preference.current_preference()
        if year is None
        else get_object_or_404(Preference, year=year)
    )
    evaluations = Evaluation.objects.filter(preference=preferences, has_answers=True)

    # Unused variables, but they are included in `locals()`
    if evaluations.count():
        if evaluations.exclude(internship_marathon_rating=0).count():
            avg_internship_marathon_rating = (
                sum(e.internship_marathon_rating for e in evaluations)
                / evaluations.exclude(internship_marathon_rating=0).count()
            )

        if evaluations.exclude(course_rating=0).count():
            avg_course_rating = (
                sum(e.course_rating for e in evaluations)
                / evaluations.exclude(course_rating=0).count()
            )

        if evaluations.exclude(visitors_rating=0).count():
            avg_visitors_rating = (
                sum(e.visitors_rating for e in evaluations) / evaluations.count()
            )

        if evaluations.exclude(interview_location_rating=0).count():
            avg_interview_location_rating = (
                sum(e.interview_location_rating for e in evaluations)
                / evaluations.exclude(interview_location_rating=0).count()
            )

        if evaluations.exclude(banquet_rating=0).count():
            avg_banquet_rating = (
                sum(e.banquet_rating for e in evaluations)
                / evaluations.exclude(banquet_rating=0).count()
            )

        percentage_want_to_come_back = (
            evaluations.filter(want_to_come_back=True).count() / evaluations.count()
        ) * 100

    title = _("Evaluation of itDAGENE")
    description = preferences.year
    prev_year = preferences.year - 1
    return render(request, "feedback/evaluations/report.html", locals())
