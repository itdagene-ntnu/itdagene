from datetime import date, time

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from itdagene.app.events.forms import EventForm
from itdagene.app.events.models import Event
from itdagene.core.models import Preference, User


class TestEventFilters(TestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create(is_superuser=True, is_staff=True)
        self.preference = Preference.objects.create(
            active=True,
            year=2031,
            start_date=date(2031, 9, 14),
            end_date=date(2031, 9, 15),
        )
        self.client.force_login(self.user)
        self.course = Event.objects.create(
            title="Course",
            date=self.preference.start_date,
            time_start=time(9, 0),
            time_end=time(10, 0),
            description="Course description",
            type=0,
            location="U1",
        )
        self.presentation = Event.objects.create(
            title="Presentation",
            date=self.preference.start_date,
            time_start=time(10, 0),
            time_end=time(11, 0),
            description="Presentation description",
            type=1,
            location="U1",
        )

    def tearDown(self):
        cache.clear()

    def test_malformed_typed_filters_return_validation_errors(self):
        url = reverse("itdagene.events.list_events")

        for field, value in (
            ("day", "not-a-date"),
            ("type", "not-an-integer"),
            ("company", "not-an-integer"),
        ):
            with self.subTest(field=field):
                response = self.client.get(url, {field: value})

                self.assertEqual(200, response.status_code)
                self.assertIn(field, response.context["filter_form"].errors)

    def test_zero_value_event_type_is_applied(self):
        response = self.client.get(
            reverse("itdagene.events.list_events"),
            {"type": "0"},
        )

        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(
            response.context["events"],
            [repr(self.course)],
        )

    def test_event_form_allows_dates_outside_the_fair_in_the_same_edition(self):
        form = EventForm(
            {
                "title": "Outside fair",
                "date": date(2031, 8, 1),
                "time_start": "09:00",
                "time_end": "10:00",
                "description": "Should not be public",
                "type": 0,
                "location": "U1",
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual("2031-01-01", form.fields["date"].widget.attrs["min"])
        self.assertEqual("2031-12-31", form.fields["date"].widget.attrs["max"])

    def test_event_form_rejects_dates_from_another_edition(self):
        form = EventForm(
            {
                "title": "Wrong edition",
                "date": date(2032, 1, 1),
                "time_start": "09:00",
                "time_end": "10:00",
                "description": "Should not be public in 2031",
                "type": 0,
                "location": "U1",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            "Datoen må være i 2031 for å vises i årets program.",
            form.errors["date"][0],
        )
        self.assertEqual("2031-01-01", form.fields["date"].widget.attrs["min"])
        self.assertEqual("2031-12-31", form.fields["date"].widget.attrs["max"])

    def test_event_form_keeps_archived_events_editable(self):
        archived_event = Event.objects.create(
            title="Archived event",
            date=date(2030, 9, 14),
            time_start=time(9, 0),
            time_end=time(10, 0),
            description="Existing event from an earlier edition",
            type=0,
            location="U1",
        )
        form = EventForm(
            {
                "title": "Updated archived event",
                "date": archived_event.date,
                "time_start": "09:00",
                "time_end": "10:00",
                "description": archived_event.description,
                "type": archived_event.type,
                "location": archived_event.location,
            },
            instance=archived_event,
        )

        self.assertTrue(form.is_valid())

    def test_event_form_uses_start_date_year_when_preference_year_is_missing(self):
        self.preference.year = None
        form = EventForm(preference=self.preference)

        self.assertEqual("2031-01-01", form.fields["date"].widget.attrs["min"])
        self.assertEqual("2031-12-31", form.fields["date"].widget.attrs["max"])

    def test_event_list_accepts_same_edition_events_outside_the_fair_dates(self):
        Event.objects.create(
            title="Outside fair",
            date=date(2031, 8, 1),
            time_start=time(9, 0),
            time_end=time(10, 0),
            description="Should not be public",
            type=0,
            location="U1",
        )

        response = self.client.get(reverse("itdagene.events.list_events"))

        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Outside fair")
        self.assertNotContains(response, "ligger utenfor messedagene")
