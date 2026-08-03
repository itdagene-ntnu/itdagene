from datetime import date

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from itdagene.core.models import Preference, User


class TestAdministrationLanguage(TestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_superuser(
            username="administrator",
            email="admin@example.com",
            password="test-password",
        )
        self.preference = Preference.objects.create(
            active=True,
            year=2026,
            start_date=date(2026, 9, 14),
            end_date=date(2026, 9, 15),
        )
        self.client.force_login(self.user)

    def tearDown(self):
        cache.clear()

    def test_settings_use_norwegian_labels_for_publication_controls(self):
        response = self.client.get(reverse("itdagene.itdageneadmin.preferences.edit"))

        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Innstillinger")
        self.assertContains(response, "Vis program")
        self.assertContains(response, "Vis stands")
        self.assertContains(response, "Skal programmet vises på nettsiden?")
        self.assertContains(
            response,
            "Skal årets publiserte standkart og standplasseringer vises på "
            "nettsiden?",
        )
        self.assertNotContains(response, "Preferences")

    def test_general_administration_navigation_is_norwegian(self):
        response = self.client.get(reverse("itdagene.itdageneadmin.landing_page"))

        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Administrasjon")
        self.assertContains(response, "Innstillinger")
        self.assertContains(response, "Grupper")
        self.assertContains(response, "Nullstill bedriftsdata")
        self.assertNotContains(response, "Reset companies")
