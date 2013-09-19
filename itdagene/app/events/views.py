from django.core.urlresolvers import reverse
from itdagene.app.events.forms import EventForm, EventTicketForm, EventTicketUpdateForm
from itdagene.app.events.models import Event, Ticket
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from itdagene.core import Preference

def public_event_list(request):
    pref = Preference.current_preference()
    day_one = Event.objects.filter(date=pref.start_date).order_by('time_start')
    day_two = Event.objects.filter(date=pref.end_date).order_by('time_start')
    return render(request, 'events/public_list.html', {'day_one': day_one, 'day_two': day_two})


@permission_required('events.change_event')
def list_events (request):
    pref = Preference.current_preference()
    events = Event.objects.filter(date__year=pref.year)
    return render(request, 'events/base.html', {'events': events})

@permission_required('events.change_event')
def view_event (request, id):
    event = get_object_or_404(Event, pk=id)
    form = EventTicketForm(instance=Ticket(event=event))
    if request.method == 'POST':
        form = EventTicketForm(request.POST, instance=Ticket(event=event))
        if form.is_valid():
            form.save()
            request.session['message'] = {'class': 'success', 'value': _('%s was saved.') % _('Ticket')}
            form = EventTicketForm(instance=Ticket(event=event))
        else:
            request.session['message'] = {'class': 'errormsg', 'value': _('%s could not be saved.') % _('Ticket')}
    return render(request, 'events/view.html', {'event': event, 'form': form})

@permission_required('events.change_event')
def edit_ticket (request, id):
    ticket = get_object_or_404(Ticket, pk=id)
    form = EventTicketUpdateForm(instance=ticket)
    if request.method == 'POST':
        form = EventTicketUpdateForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            request.session['message'] = {'class': 'success', 'value': _('%s was saved.') % _('Ticket')}
        else:
            request.session['message'] = {'class': 'errormsg', 'value': _('%s could not be saved.') % _('Ticket')}
        return redirect(reverse('view_event', args=[ticket.event.pk]))
    return render(request, 'events/tickets/edit.html', {'form': form})

@permission_required('events.change_event')
def edit_event (request, id=None):
    event = None
    if id: event = get_object_or_404(Event, pk=id)
    form = EventForm(instance=event)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            request.session['message'] = {'class': 'success', 'value': _('%s was saved.') % event.title}
            return redirect(reverse('view_event', args=[event.pk]))
        else:
            request.session['message'] = {'class': 'errormsg', 'value': _('%s could not be saved.') % form['title'].data}
    return render(request, 'events/form.html', {'event': event, 'form': form})
