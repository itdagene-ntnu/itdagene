from typing import Any

from django.contrib.auth.decorators import permission_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from itdagene.app.workschedule.forms import WorkerForm, WorkScheduleForm
from itdagene.app.workschedule.models import Worker, WorkerInSchedule, WorkSchedule


@permission_required("workschedule.add_worker")
def add_worker(request: HttpRequest) -> HttpResponse:
    form = WorkerForm()
    if request.method == "POST":
        form = WorkerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("itdagene.workschedule.list"))
    return render(request, "worker/form.html", {"form": form, "title": _("Add Worker")})


@permission_required("workschedule.add_workschedule")
def add_task(request: HttpRequest) -> HttpResponse:
    form = WorkScheduleForm()
    if request.method == "POST":
        form = WorkScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("itdagene.workschedule.list"))
    return render(
        request,
        "workschedule/form.html",
        {"form": form, "title": _("Add Work Schedule")},
    )


@permission_required("workschedule.change_worker")
def edit_worker(request: HttpRequest, id: Any) -> HttpResponse:
    ws = get_object_or_404(Worker, pk=id)
    form = WorkerForm(instance=ws)
    if request.method == "POST":
        form = WorkerForm(request.POST, instance=ws)
        if form.is_valid():
            form.save()
            return redirect(reverse("itdagene.workschedule.list"))

    return render(
        request,
        "worker/form.html",
        {"form": form, "title": _("Edit Worker"), "description": str(ws), "worker": ws},
    )


@permission_required("workschedule.change_workschedule")
def edit_task(request: HttpRequest, id: Any) -> HttpResponse:
    ws = get_object_or_404(WorkSchedule, pk=id)
    form = WorkScheduleForm(instance=ws)
    if request.method == "POST":
        form = WorkScheduleForm(request.POST, instance=ws)
        if form.is_valid():
            form.save()
            return redirect(reverse("itdagene.workschedule.list"))

    return render(
        request,
        "workschedule/form.html",
        {"form": form, "title": _("Edit Task"), "description": str(ws), "task": ws},
    )


# @permission_required('workschedule.view_workschedule')
# def list(request: HttpRequest) -> HttpResponse:
#    workers = Worker.objects.filter(preference=Preference.current_preference().year)
#    pref = Preference.current_preference()
#    start_date = pref.start_date
#    end_date = pref.end_date
#    days: list = []
#    number = 1
#    for dt in rrule(DAILY, dtstart=start_date, until=end_date):
#        days.append(
#            {
#                'number': number,
#                'list': WorkSchedule.objects.filter(date=dt).order_by('date'),
#                'date': dt
#            }
#        )
#        number += 1
#    other = (
#        WorkSchedule
#        .objects
#        .filter(date__year=pref.year)
#        .exclude(date__gte=start_date, date__lte=end_date)
#        .order_by('date')
#    )
#    return render(
#        request, 'workschedule/list.html',
#        {
#            'other': other,
#            'days': days,
#            'title': _('Work Schedule'),
#            'workers': workers
#        }
#    )


@permission_required("workschedule.view_workschedule")
def view_task(request: HttpRequest, id: Any) -> HttpResponse:
    task = get_object_or_404(WorkSchedule, pk=id)
    attendance = WorkerInSchedule.objects.filter(schedule=task)
    return render(
        request,
        "workschedule/view.html",
        {
            "task": task,
            "attendance": attendance,
            "title": _("Task"),
            "description": str(task),
        },
    )


@permission_required("workschedule.change_worker")
def change_attendance(request: Any, id: Any) -> HttpResponse:
    worker = get_object_or_404(WorkerInSchedule, pk=id)
    worker.has_met = not worker.has_met
    worker.save()
    return redirect(
        reverse("itdagene.workschedule.view_task", args=[worker.schedule.pk])
    )


# @permission_required('workschedule.view_workschedule')
# def view_worker(request: HttpRequest, id: Any) -> HttpResponse:
#    worker = get_object_or_404(Worker, pk=id)
#    return render(
#        request, 'worker/view.html',
#        {
#            'worker': worker,
#            'title': _('Worker'),
#            'description': worker.name
#        }
#    )
