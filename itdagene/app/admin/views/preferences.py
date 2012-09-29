from django.core.urlresolvers import reverse
from itdagene.app.admin.forms import PreferenceForm
from django.contrib.auth.decorators import permission_required
from itdagene.core.models import Preference
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.shortcuts import render

@permission_required('core.change_preference')
def view (request, year=None):
    if not year:
        pref = Preference.current_preference()
    else:
        pref = get_object_or_404(Preference, year=year)
    return render(request, 'adm/preferences/view.html',
                             {'pref': pref})

@permission_required('core.change_preference')
def edit (request, year=None):
    if not year:
        pref = Preference.current_preference()
    else:
        pref = get_object_or_404(Preference, year=year)
    form = PreferenceForm(instance=pref)
    if request.method == 'POST':
        form = PreferenceForm(request.POST,instance=pref)
        if form.is_valid():
            form.save()
            redirect(reverse('app.admin.views.preferences.view', args=[year]))
    return render(request, 'adm/preferences/edit.html',
                             {'pref': pref,
                              'form': form})