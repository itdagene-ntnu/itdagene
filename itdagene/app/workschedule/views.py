from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from itdagene.app.workschedule.forms import WorkScheduleForm, WorkerForm, WorkerHasMetForm
from itdagene.app.workschedule.models import WorkSchedule, Worker
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from itdagene.core.models import Preference

def public_list(request):
    workers = Worker.objects.all()
    pref = Preference.objects.get(active=True)

    dayOne = WorkSchedule.objects.filter(date=pref.start_date).order_by('start_time')
    dayTwo = WorkSchedule.objects.filter(date=pref.end_date).order_by('start_time')
    other = WorkSchedule.objects.filter(date__year=pref.year).exclude(date=pref.start_date).exclude(date=pref.end_date).order_by('date')

    return render(request, 'workschedule/public_list.html',{'dayOne': dayOne, 'dayTwo': dayTwo, 'other': other})

def view_public_task(request, id):
    task = get_object_or_404(WorkSchedule, pk=id)
    return render(request, 'workschedule/view_public.html', {'task': task})

@permission_required('workschedule.view_workschedule')
def list(request):
    workers = Worker.objects.all()
    pref = Preference.objects.get(active=True)

    dayOne = WorkSchedule.objects.filter(date=pref.start_date).order_by('start_time')
    dayTwo = WorkSchedule.objects.filter(date=pref.end_date).order_by('start_time')
    other = WorkSchedule.objects.filter(date__year=pref.year).exclude(date=pref.start_date).exclude(date=pref.end_date).order_by('date')

    return render(request, 'workschedule/list.html',{'dayOne': dayOne, 'dayTwo': dayTwo, 'other': other})

@permission_required('workschedule.view_workschedule')
def email_list(request):
    workers = Worker.objects.exclude(in_schedules=None)
    return render(request, 'workschedule/emaillist.html',{'workers': workers})

@permission_required('workschedule.view_workschedule')
def view_task(request, id):
    task = get_object_or_404(WorkSchedule, pk=id)
    return render(request, 'workschedule/view.html', {'task': task})

@permission_required('workschedule.view_workschedule')
def view_worker(request, id):
    worker = get_object_or_404(Worker, pk=id)
    return render(request, 'worker/view.html', {'worker': worker})

@permission_required('workschedule.view_workschedule')
def add_task(request):
    if request.method == 'POST':
        form = WorkScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return list(request)
        else:
            return render(request, 'workschedule/form.html',
                             {'form': form})
    return edit_task(request, None)

@permission_required('workschedule.view_workschedule')
def has_met(request, id):
    ws = get_object_or_404(WorkSchedule, pk=id)
    form = WorkerHasMetForm(instance=ws)
    if request.method == 'POST':
        form = WorkerHasMetForm(request.POST, instance=ws)
        if form.is_valid():
            form.save()

    return render(request, 'workschedule/form.html', {'form': form})

@permission_required('workschedule.view_workschedule')
def add_worker(request):
    if request.method == 'POST':
        form = WorkerForm(request.POST)
        if form.is_valid():
            form.save()
            return list(request)
        else:
            return render(request, 'worker/form.html',
                             {'form': form})
    return edit_worker(request, None)

@permission_required('workschedule.view_worker')
def edit_worker(request, id):
    form = WorkerForm()
    if id:
        ws = get_object_or_404(Worker,pk=id)
        form = WorkerForm(instance=ws)
        if request.method == 'POST':
            form = WorkerForm(request.POST, instance=ws)
            if form.is_valid():
                form.save()

    return render(request, 'worker/form.html',
                             {'form': form})

@permission_required('workschedule.view_workschedule')
def edit_task (request, id):
    form = WorkScheduleForm()
    if id:
        ws = get_object_or_404(WorkSchedule,pk=id)
        form = WorkScheduleForm(instance=ws)
        if request.method == 'POST':
            form = WorkScheduleForm(request.POST, instance=ws)
            if form.is_valid():
                form.save()

    return render(request, 'workschedule/form.html',
                             {'form': form})

