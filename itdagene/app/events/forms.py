from django.forms.models import ModelForm

from itdagene.app.company.models import Company
from itdagene.app.events.models import Event, Ticket


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = (
            'title', 'date', 'time_start', 'time_end', 'description', 'type', 'location',
            'is_internal', 'company', 'uses_tickets', 'max_participants'
        )


class EventTicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ('company', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(EventTicketForm, self).__init__(*args, **kwargs)
        companies = Company.objects.filter(active=True)
        self.fields['company'].queryset = companies
