from datetime import date, time

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

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
