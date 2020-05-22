from django.contrib.auth.decorators import permission_required
from django.contrib.messages import SUCCESS, add_message
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from itdagene.app.todo.forms import TodoForm
from itdagene.app.todo.models import Todo


@permission_required("todo.add_todo")
def add_todo(request):
    form = TodoForm()
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.save(notify_subscribers=False)
            add_message(request, SUCCESS, _("Todo added."))
            return redirect(reverse("itdagene.frontpage"))
    return render(
        request, "todo/todo_form.html", {"form": form, "title": _("Add Todo")}
    )


@permission_required("todo.change_todo")
def change_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    form = TodoForm(instance=todo)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.save(notify_subscribers=False)
            add_message(request, SUCCESS, _("Todo changed."))
            return redirect(reverse("itdagene.frontpage"))
    return render(
        request, "todo/todo_form.html", {"form": form, "title": _("Change Todo")}
    )


@permission_required("todo.delete_todo")
def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)

    if request.method == "POST":
        todo.delete()
        add_message(request, SUCCESS, _("Todo deleted."))
        return redirect(reverse("itdagene.frontpage"))

    return render(
        request, "todo/delete_todo.html", {"todo": todo, "title": _("Delete Todo")}
    )


def view_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    return render(
        request,
        "todo/view_todo.html",
        {"todo": todo, "title": _("Todo"), "now": timezone.now()},
    )


def change_status(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.finished = not todo.finished
    todo.save(notify_subscribers=False)
    return redirect(reverse("itdagene.frontpage"))
