from django import forms
from django.core.cache import cache
from django.forms.models import ModelForm
from django.forms.util import ErrorList
from django.utils.translation import ugettext as _

from itdagene.app.company.models import Company
from itdagene.app.events.models import Event, Ticket


class EventForm(ModelForm):
    class Meta:
        model = Event


class EventTicketForm (ModelForm):
    class Meta:
        model = Ticket
        exclude = ('event', )

    def __init__(self, *args, **kwargs):
        super(EventTicketForm, self).__init__(*args, **kwargs)
        companies = Company.objects.filter(active=True)
        self.fields['company'].queryset = companies
