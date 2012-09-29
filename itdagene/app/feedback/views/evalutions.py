# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _, activate
from itdagene.app.feedback.forms import EvaluationForm
from itdagene.app.feedback.models import Evaluation, EvaluationHash


def handle_evaluation(request, hash):
    activate('nb')

    hash = get_object_or_404(EvaluationHash, hash=hash)
    instance = Evaluation(hash=hash)


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

