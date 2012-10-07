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
def report (request):
    preferences = Preference.current_preference()
    evaluations = Evaluation.objects.filter(hash__preference=preferences)
    return render(request, 'feedback/evaluations/report.html',{
        'evaluations': evaluations,
        'preferences': preferences
    })
