from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from itdagene.app.workschedule.forms import WorkScheduleForm
from itdagene.app.workschedule.models import WorkSchedule, Worker
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

@permission_required('workschedule.view_workschedule')
def list(request):
    workers = Worker.objects.all()

    return render(request, 'workschedule/list.html',{'workers': workers})

@permission_required('workschedule.view_workschedule')
def email_list(request):
    workers = Worker.objects.exclude(in_schedules=None)
    return render(request, 'workschedule/emaillist.html',{'workers': workers})

@permission_required('workschedule.view_workschedule')
def has_met(request, id):
    instance = get_object_or_404(WorkSchedule, id=id)
    instance.has_met = True
    instance.save()
    return render(request, 'base.html')

@permission_required('workschedule.view_workschedule')
def add(request):
    if request.method == 'POST':
        form = WorkScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return list(request)
        else:
            return render(request, 'workschedule/form.html',
                             {'form': form})
    return edit(request, None)

@permission_required('workschedule.view_workschedule')
def edit (request, id):
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
