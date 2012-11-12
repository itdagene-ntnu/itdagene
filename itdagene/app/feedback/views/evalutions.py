# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _, activate
from itdagene.app.feedback.forms import EvaluationForm
from itdagene.app.feedback.models import Evaluation, EvaluationHash
from itdagene.core import Preference

EN = [1065]

def handle_evaluation(request, hash):
    hash = get_object_or_404(EvaluationHash, hash=hash)
    try:
        instance = Evaluation.objects.get(hash=hash)
    except (TypeError, Evaluation.DoesNotExist):
        instance = Evaluation(hash=hash)

    if hash.company_id in EN:
        activate('en')
    else:
        activate('nb')

    form = EvaluationForm(instance=instance)
    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, _('Thank you'))

            return render(request, 'feedback/evaluations/handle_evaluate.html')

    return render(request, 'feedback/evaluations/handle_evaluate.html',{
        'form': form,
        'company': instance.hash.company
    })

@login_required
def report (request, year=None):
    if year is None:
        preferences = Preference.current_preference()
    else:
        preferences = get_object_or_404(Preference, year=year)
    evaluations = Evaluation.objects.filter(hash__preference=preferences)

    if evaluations.count():
        if evaluations.exclude(internship_marathon_rating=0).count():
            avg_internship_marathon_rating = sum([e.internship_marathon_rating for e in evaluations])/evaluations.exclude(internship_marathon_rating=0).count()

        if evaluations.exclude(course_rating=0).count():
            avg_course_rating = sum([e.course_rating for e in evaluations])/evaluations.exclude(course_rating=0).count()

        if evaluations.exclude(visitors_rating=0).count():
            avg_visitors_rating = sum([e.visitors_rating for e in evaluations])/evaluations.count()

        if evaluations.exclude(interview_location_rating=0).count():
            avg_interview_location_rating = sum([e.interview_location_rating for e in evaluations])/evaluations.exclude(interview_location_rating=0).count()

        if evaluations.exclude(banquet_rating=0).count():
            avg_banquet_rating = sum([e.banquet_rating for e in evaluations])/evaluations.exclude(banquet_rating=0).count()

        percentage_want_to_come_back = (evaluations.filter(want_to_come_back=True).count()/evaluations.count())*100

    return render(request, 'feedback/evaluations/report.html', locals())
