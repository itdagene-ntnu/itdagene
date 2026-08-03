from datetime import date

from django import forms
from django.forms.models import ModelForm
from django.utils.translation import gettext_lazy as _

from itdagene.app.company.models import Company
from itdagene.app.events.models import EVENT_TYPES, Event, Ticket
from itdagene.core.models import Preference


class EventFilterForm(forms.Form):
    day = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    type = forms.TypedChoiceField(
        choices=(("", _("All")),) + EVENT_TYPES,
        coerce=int,
        empty_value=None,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    internal = forms.TypedChoiceField(
        choices=(("", _("All")), ("0", _("Public")), ("1", _("Internal"))),
        coerce=lambda value: value == "1",
        empty_value=None,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    company = forms.ModelChoiceField(
        queryset=Company.objects.none(),
        required=False,
        empty_label=_("All"),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, edition_year, **kwargs) -> None:
        super(EventFilterForm, self).__init__(*args, **kwargs)
        self.fields["company"].queryset = (
            Company.objects.filter(event__date__year=edition_year)
            .order_by("name", "pk")
            .distinct()
        )


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = (
            "title",
            "date",
            "time_start",
            "time_end",
            "cover_image",
            "description",
            "type",
            "location",
            "is_internal",
            "company",
            "stand",
            "uses_tickets",
            "max_participants",
        )
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time_start": forms.TimeInput(attrs={"type": "time"}),
            "time_end": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, preference=None, **kwargs) -> None:
        super(EventForm, self).__init__(*args, **kwargs)
        self.preference = preference or Preference.current_preference()
        self.edition_year = self.preference.year or self.preference.start_date.year
        self.fields["date"].widget.attrs.update(
            {
                "min": date(self.edition_year, 1, 1).isoformat(),
                "max": date(self.edition_year, 12, 31).isoformat(),
            }
        )
        if not self.is_bound and not self.instance.pk:
            self.fields["date"].initial = self.preference.start_date

    def clean_date(self):
        event_date = self.cleaned_data["date"]
        keeps_archived_date = self.instance.pk and event_date == self.instance.date
        if event_date.year == self.edition_year or keeps_archived_date:
            return event_date
        raise forms.ValidationError(
            _("Datoen må være i %(year)s for å vises i årets program."),
            params={"year": self.edition_year},
        )


class EventTicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ("company", "first_name", "last_name", "email")

    def __init__(self, *args, **kwargs) -> None:
        super(EventTicketForm, self).__init__(*args, **kwargs)
        companies = Company.objects.filter(active=True)
        self.fields["company"].queryset = companies
