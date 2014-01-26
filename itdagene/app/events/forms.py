from django.forms.models import ModelForm
from itdagene.app.company.models import Company
from itdagene.app.events.models import Event, Ticket
from django.contrib.auth.models import User
from django.core.cache import cache
from django import forms
from django.utils.translation import ugettext as _
from django.forms.util import ErrorList


class EventForm (ModelForm):
    class Meta:
        model = Event

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if field.widget.is_required:
                field.widget.attrs['required'] = 'required'
        self.fields['date'].widget.attrs['type'] = 'date'
        self.fields['date'].widget.attrs.update({'type': 'date', 'placeholder': 'YYYY-MM-DD'})
        self.fields['time_start'].widget.attrs.update({'placeholder': 'HH:MM'})
        self.fields['time_end'].widget.attrs.update({'placeholder': 'HH:MM'})


class EventTicketForm (ModelForm):
    class Meta:
        model = Ticket
        exclude = ('user')

    def __init__(self, *args, **kwargs):
        super(EventTicketForm, self).__init__(*args, **kwargs)
#        users = User.objects.filter(is_active=True).order_by('first_name')
#        self.fields['user'].choices = [('', '----')] + [(user.pk, user.get_full_name()) for user in users]
        self.fields['event'].widget = forms.HiddenInput()
        companies = cache.get('companies')
        if not companies:
            companies = Company.objects.filter(active=True)
            cache.set('companies', companies)
        self.fields['company'].queryset = companies

    def clean(self):
        cleaned_data = super(EventTicketForm, self).clean()
        count = Ticket.objects.filter(event=cleaned_data['event'], company=cleaned_data['company']).count()
        if Ticket.objects.filter(event=cleaned_data['event']).count() >= self.cleaned_data['event'].max_participants:
            self._errors["company"] = ErrorList([_('No tickets left')])
        if count >= 1 and not cleaned_data['company'].partner:
            if Ticket.extra_tickets_used(cleaned_data['event']) >= 23:
                self._errors["company"] = ErrorList([_('No extra-tickets left')])
            if count >= 2:
                self._errors["company"] = ErrorList([_('Company has no extra-tickets left')])
        elif count >= 3 and cleaned_data['company'].partner:
            if Ticket.extra_tickets_used(cleaned_data['event']) >= 23:
                self._errors["company"] = ErrorList([_('No extra-tickets left')])
            if count >= 4:
                self._errors["company"] = ErrorList([_('Company has no extra-tickets left')])
        return cleaned_data

class EventTicketUpdateForm (ModelForm):
    class Meta:
        model = Ticket
        exclude = ('user')

    def __init__(self, *args, **kwargs):
        super(EventTicketUpdateForm, self).__init__(*args, **kwargs)
        self.fields['event'].widget = forms.HiddenInput()
        companies = cache.get('companies')
        if not companies:
            companies = Company.objects.filter(active=True)
            cache.set('companies', companies)
        self.fields['company'].queryset = companies
