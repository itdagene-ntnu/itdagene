from django.core.urlresolvers import reverse
from itdagene.app.events.forms import EventForm, EventTicketForm
from itdagene.app.events.models import Event, Ticket
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from itdagene.core.models import Preference
from itdagene.core.decorators import staff_required
from django.contrib.messages import add_message, SUCCESS


@staff_required()
def list_events(request):
    pref = Preference.current_preference()
    events = Event.objects.filter(date__year=pref.year)
    return render(request, 'events/base.html', {'events': events, 'title': _('Events')})


@permission_required('events.add_event')
def add_event(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            add_message(request, SUCCESS, _('Event added.'))
            return redirect(event.get_absolute_url())
    return render(request, 'events/form.html', {'form': form, 'title': _('Add Event')})


@permission_required('events.change_event')
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(instance=event)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            add_message(request, SUCCESS, _('Event saved.'))
            return redirect(event.get_absolute_url())
    return render(request, 'events/form.html', {'event': event, 'form': form, 'title': _('Edit Event'), 'description': str(event)})


@staff_required()
def view_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = EventTicketForm(instance=Ticket(event=event))
    if request.method == 'POST':
        form = EventTicketForm(request.POST, instance=Ticket(event=event))
        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, _('Ticket was saved.'))
            form = EventTicketForm(instance=Ticket(event=event))
    return render(request, 'events/view.html', {'event': event, 'form': form, 'title': _('Event'), 'description': str(event)})


@staff_required()
def edit_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    form = EventTicketForm(instance=ticket)
    if request.method == 'POST':
        form = EventTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, _('Ticket saved.'))
            return redirect(ticket.event.get_absolute_url())

    return render(request, 'events/form.html', {'form': form, 'title': _('Edit Ticket'), 'description': str(ticket)})


