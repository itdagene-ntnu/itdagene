from typing import Any

from django.contrib.auth.decorators import permission_required
from django.contrib.messages import SUCCESS, add_message
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from itdagene.app.events.forms import EventFilterForm, EventForm, EventTicketForm
from itdagene.app.events.models import Event, Ticket
from itdagene.core.decorators import staff_required
from itdagene.core.models import Preference


@staff_required()
def list_events(request: HttpRequest) -> HttpResponse:
    edition_year = Preference.current_preference().year
    events = Event.objects.filter(date__year=edition_year).select_related(
        "company", "stand"
    )
    filter_form = EventFilterForm(
        request.GET or None,
        edition_year=edition_year,
    )
    if filter_form.is_valid():
        day = filter_form.cleaned_data["day"]
        event_type = filter_form.cleaned_data["type"]
        internal = filter_form.cleaned_data["internal"]
        company = filter_form.cleaned_data["company"]
        search = filter_form.cleaned_data["q"]
        if day:
            events = events.filter(date=day)
        if event_type is not None:
            events = events.filter(type=event_type)
        if internal is not None:
            events = events.filter(is_internal=internal)
        if company:
            events = events.filter(company=company)
        if search:
            events = events.filter(title__icontains=search)
    return render(
        request,
        "events/base.html",
        {
            "events": events.order_by("date", "time_start", "time_end", "title"),
            "filter_form": filter_form,
            "title": _("Events"),
        },
    )


@permission_required("events.add_event")
def add_event(request: HttpRequest) -> HttpResponse:
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            add_message(request, SUCCESS, _("Event added."))
            return redirect(event.get_absolute_url())
    return render(request, "events/form.html", {"form": form, "title": _("Add Event")})


@permission_required("events.change_event")
def edit_event(request: HttpRequest, pk: Any) -> HttpResponse:
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(instance=event)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save()
            add_message(request, SUCCESS, _("Event saved."))
            return redirect(event.get_absolute_url())
    return render(
        request,
        "events/form.html",
        {
            "event": event,
            "form": form,
            "title": _("Edit Event"),
            "description": str(event),
        },
    )


@permission_required("events.delete_event")
def delete_event(request: HttpRequest, pk: Any) -> HttpResponse:
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        event.delete()
        add_message(request, SUCCESS, _("Event deleted."))
        return redirect(reverse("itdagene.events.list_events"))
    return render(
        request,
        "events/delete.html",
        {"event": event, "title": _("Delete Event"), "description": str(event)},
    )


@staff_required()
def view_event(request: HttpRequest, pk: Any) -> HttpResponse:
    event = get_object_or_404(Event, pk=pk)
    form = EventTicketForm(instance=Ticket(event=event))
    if request.method == "POST":
        form = EventTicketForm(request.POST, instance=Ticket(event=event))
        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, _("Ticket was saved."))
            form = EventTicketForm(instance=Ticket(event=event))
    return render(
        request,
        "events/view.html",
        {"event": event, "form": form, "title": _("Event"), "description": str(event)},
    )


@staff_required()
def edit_ticket(request: HttpRequest, pk: Any) -> HttpResponse:
    ticket = get_object_or_404(Ticket, pk=pk)
    form = EventTicketForm(instance=ticket)
    if request.method == "POST":
        form = EventTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, _("Ticket saved."))
            return redirect(ticket.event.get_absolute_url())
    return render(
        request,
        "events/form.html",
        {"form": form, "title": _("Edit Ticket"), "description": str(ticket)},
    )
