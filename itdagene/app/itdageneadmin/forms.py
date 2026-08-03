from django import forms
from django.contrib.auth.models import Group
from django.forms import CharField, IntegerField
from django.forms.forms import Form
from django.forms.models import ModelForm

from itdagene.core.models import Preference, User


class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = (
            "username",
            "password",
            "user_permissions",
            "last_login",
            "date_joined",
        )
        labels = {
            "first_name": "Fornavn",
            "last_name": "Etternavn",
            "email": "E-post",
            "phone": "Telefonnummer",
            "linkedin": "LinkedIn",
            "photo": "Bilde",
            "language": "Språk",
            "mail_notification": "E-postvarsler",
            "year": "Aktivt år",
            "is_active": "Aktiv",
            "is_staff": "Administrator",
            "is_superuser": "Superbruker",
            "groups": "Grupper",
        }


class RegisterUserForm(Form):
    username = CharField(max_length=8, label="Brukernavn")
    first_name = CharField(label="Fornavn")
    last_name = CharField(label="Etternavn")
    phone = IntegerField(label="Telefonnummer")


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ("name", "permissions")
        labels = {"name": "Navn", "permissions": "Tilganger"}


class AddUserToGroupForm(Form):
    username = CharField(label="Brukernavn")


class PreferenceForm(ModelForm):
    class Meta:
        model = Preference
        exclude = ("active",)
        labels = {
            "development_mode": "Utviklermodus",
            "year": "År",
            "start_date": "Startdato",
            "end_date": "Sluttdato",
            "nr_of_stands": "Antall stands per dag",
            "view_sp": "Vis samarbeidspartnere",
            "view_hsp": "Vis hovedsamarbeidspartner",
            "view_companies": "Vis alle bedrifter",
            "hsp_intro": "Introduksjon av hovedsamarbeidspartner",
            "hsp_video": "Video-URL for hovedsamarbeidspartner",
            "hsp_poster": "Bilde-URL for hovedsamarbeidspartner",
            "show_interest_form": "Vis interesseskjema",
            "interest_form_url": "URL til interesseskjema",
            "program_published": "Vis program",
            "stands_published": "Vis stands",
            "venue": "Sted",
            "event_start_time": "Starttid for itDAGENE (nedtelling)",
        }
        help_texts = {
            "development_mode": (
                "Setter nettsiden i utviklermodus. Den offentlige siden blir "
                "utilgjengelig."
            ),
            "nr_of_stands": "Dette gjelder per dag, ikke totalt.",
            "view_sp": "Skal samarbeidspartnerne vises på nettsiden?",
            "view_hsp": "Skal hovedsamarbeidspartneren vises på nettsiden?",
            "view_companies": "Skal årets bedrifter vises på nettsiden?",
            "hsp_intro": (
                "Introduksjonen vises sammen med hovedsamarbeidspartneren på "
                "forsiden."
            ),
            "hsp_video": "URL til hovedsamarbeidspartnerens introduksjonsvideo.",
            "hsp_poster": "URL til bildet som vises før videoen starter.",
            "show_interest_form": (
                "Skal interesseskjemaet for bedrifter vises på nettsiden?"
            ),
            "interest_form_url": "URL til bedriftenes interesseskjema.",
            "program_published": "Skal programmet vises på nettsiden?",
            "stands_published": (
                "Skal årets publiserte standkart og standplasseringer vises på "
                "nettsiden?"
            ),
        }
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "event_start_time": forms.TimeInput(attrs={"type": "time"}),
        }
