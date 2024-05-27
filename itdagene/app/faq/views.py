from django.shortcuts import render

from django.utils.translation import gettext_lazy as _
from itdagene.app.faq.forms import QuestionForm
from django.contrib.messages import SUCCESS, add_message
from django.shortcuts import get_object_or_404, redirect, render, reverse

from itdagene.app.faq.models import Question

def list_questions(request):
    questions = Question.objects.all()
    return render(request, "faq/base.html", {"questions": questions, "title": _("All Questions")})

def add(request):
    form = QuestionForm()
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            add_message(request, SUCCESS, _("Question added."))
            return redirect(reverse("itdagene.faq.list_questions"))
    return render(request, "faq/form.html", {"form": form, "title": _("Add Question")})

def edit(request, pk):
    question = get_object_or_404(Question, pk=pk)
    form = QuestionForm(instance=question)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            add_message(request, SUCCESS, _("Question saved."))
            return redirect(reverse("itdagene.faq.list_questions"))
    return render(
        request,
        "faq/form.html",
        {
            "question": question,
            "form": form,
            "title": _("Edit Question"),
            "description": question,
        },
    )
