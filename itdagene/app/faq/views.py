from django.contrib.auth.decorators import permission_required
from django.contrib.messages import SUCCESS, add_message
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils.translation import gettext_lazy as _

from itdagene.app.faq.forms import QuestionForm
from itdagene.app.faq.models import Question


def list_questions(request):
    questions = Question.objects.all()
    return render(
        request, "faq/base.html", {"questions": questions, "title": _("All Questions")}
    )


@permission_required("faq.add_question")
def add_question(request):
    form = QuestionForm()
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, _("Question added."))
            return redirect(reverse("itdagene.faq.list_questions"))
    return render(request, "faq/form.html", {"form": form, "title": _("Add Question")})


@permission_required("faq.edit_question")
def edit_question(request, pk):
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
        },
    )


@permission_required("faq.delete_question")
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        question.delete()
        add_message(request, SUCCESS, _("Question deleted."))
        return redirect(reverse("itdagene.faq.list_questions"))
    return render(
        request,
        "faq/delete.html",
        {
            "question": question,
            "title": _("Delete Question"),
            "description": str(question),
        },
    )
