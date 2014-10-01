# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, get_list_or_404, Http404, redirect
from django.utils.translation import ugettext_lazy as _, activate
from itdagene.app.feedback.forms import EvaluationForm
from itdagene.app.feedback.models import Evaluation
from itdagene.core import Preference
from itdagene.core.decorators import staff_required
from django.conf import settings
from itdagene.app.company.models import Company
from django.contrib.messages import *
from django.core.urlresolvers import reverse

EN = [1065]


def handle_evaluation(request, company):
    company = get_object_or_404(Company, pk=company, user=request.user)
    (created, evaluation) = Evaluation.get_or_create(company=company, preference=Preference.current_preference())
    form = EvaluationForm(instance=evaluation)
    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, _('Thank you for your evaluation.'))
            return redirect(reverse('itdagene.app.frontpage.views.inside'))

    return render(request, 'feedback/evaluations/handle_evaluate.html',{
        'title': _('Evaluate'),
        'description': settings.SITE['name'] + ' ' + str(Preference.current_preference().year),
        'form': form
    })


@staff_required()
def report (request, year=None):
    if year is None:
        preferences = Preference.current_preference()
    else:
        preferences = get_object_or_404(Preference, year=year)
    evaluations = Evaluation.objects.filter(preference=preferences)

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

    title = _('Evaluation of itDAGENE')
    description = preferences.year

    return render(request, 'feedback/evaluations/report.html', locals())
