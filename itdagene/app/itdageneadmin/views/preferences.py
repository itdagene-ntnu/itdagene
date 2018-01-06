from django.contrib.auth.decorators import permission_required
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from itdagene.app.itdageneadmin.forms import PreferenceForm
from itdagene.core.models import Preference


@permission_required('core.change_preference')
def edit(request):
    current_pref = Preference.current_preference()
    current_year = current_pref.year
    form = PreferenceForm(instance=current_pref)
    if request.method == 'POST':
        form = PreferenceForm(request.POST, instance=current_pref)
        if form.is_valid():
            preference = form.save(commit=False)
            preference.active = True
            if preference.year != current_year:
                preference, created = Preference.objects.get_or_create(
                    year=preference.year, defaults={
                        'active': True,
                        'start_date': '%s-09-10' % preference.year,
                        'end_date': '%s-09-11' % preference.year
                    }
                )
            else:
                preference.save(log_it=False, notify_subscribers=False)

            for peference_object in Preference.objects.exclude(id=preference.id):
                peference_object.active = False
                peference_object.save(log_it=False, notify_subscribers=False)

            cache.set('pref', preference)
            return redirect(reverse('itdagene.itdageneadmin.preferences.edit'))
    return render(
        request, 'admin/preferences/edit.html', {
            'pref': current_pref,
            'form': form,
            'title': _('Preferences')
        }
    )
