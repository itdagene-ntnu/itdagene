from datetime import date

from django.core.cache import cache
from django.test import TestCase

from itdagene.core.models import Preference, User


class TestPreference(TestCase):
    def setUp(self) -> None:
        cache.clear()
        User.objects.create(is_superuser=True)

    def tearDown(self) -> None:
        cache.clear()

    def test_get_preference_by_year_returns_matching_active_preference(self) -> None:
        preference = Preference.objects.create(
            active=True,
            year=2031,
            start_date=date(2031, 9, 14),
            end_date=date(2031, 9, 15),
        )

        self.assertEqual(
            preference,
            Preference.get_preference_by_year(preference.year),
        )

    def test_current_preference_fails_fast_when_multiple_editions_are_active(
        self,
    ) -> None:
        for year in (2031, 2032):
            Preference.objects.create(
                active=True,
                year=year,
                start_date=date(year, 9, 14),
                end_date=date(year, 9, 15),
            )
        cache.clear()

        with self.assertRaises(Preference.MultipleObjectsReturned):
            Preference.current_preference()
