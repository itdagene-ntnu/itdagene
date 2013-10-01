from itdagene.core import Preference
from itdagene.app.experiences.forms import ExperienceForm
from itdagene.app.experiences.models import Experience
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render

@permission_required('meetings.change_meeting')
def list(request):
    experience_lists = []

    for pref in Preference.objects.all().order_by('-year'):
    	experience_lists.append((pref.year, Experience.objects.filter(year__year=pref.year).order_by('position')))

    return render(request, 'experiences/base.html',
                             {'experience_lists': experience_lists,})

@permission_required('meetings.change_meeting')
def view(request, id):
	experience = get_object_or_404(Experience, pk=id)
	return render(request, 'experiences/view.html',
							 {'experience': experience})

@permission_required('meetings.change_meeting')
def add(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            form.save()
            return list(request)
        else:
            return render(request, 'experiences/form.html',
                             {'form': form})
    return edit(request, None)

@permission_required('meetings.change_meeting')
def edit(request, id):
    form = ExperienceForm()
    if id:
        es = get_object_or_404(Experience, pk=id)
        form = ExperienceForm(instance=es)
        if request.method == 'POST':
            form = ExperienceForm(request.POST, instance=es)
            if form.is_valid():
                form.save()
                return view(request, id)

    return render(request, 'experiences/form.html',
                             {'form': form})
