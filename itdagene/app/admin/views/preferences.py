from django.core.urlresolvers import reverse
from itdagene.app.admin.forms import PreferenceForm
from django.contrib.auth.decorators import permission_required
from itdagene.core.models import Preference
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _


@permission_required('core.change_preference')
def view (request, year=None):
    if not year:
        pref = Preference.current_preference()
    else:
        pref = get_object_or_404(Preference, year=year)
    return render(request, 'admin/preferences/view.html', {'pref': pref, 'title':_('Preferences') })

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
            return redirect(reverse('itdagene.app.admin.views.preferences.view'))
    return render(request, 'admin/preferences/edit.html', {'pref': pref, 'form': form, 'title':_('Edit Preferences') })