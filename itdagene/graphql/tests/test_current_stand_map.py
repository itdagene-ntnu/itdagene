import shutil
import tempfile
from datetime import date
from decimal import Decimal

from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.timezone import now
from graphene.test import Client

from itdagene.app.company.models import Company
from itdagene.app.stands.models import StandMap, StandMapRelease, StandPlacement
from itdagene.core.models import Preference, User
from itdagene.graphql.schema import schema


class TestCurrentStandMap(TestCase):
    def setUp(self):
        cache.clear()
        self.media_root = tempfile.mkdtemp()
        self.media_override = override_settings(MEDIA_ROOT=self.media_root)
        self.media_override.enable()
        self.user = User.objects.create(is_superuser=True)
        self.year = now().year + 5
        self.preference = Preference.objects.create(
            active=True,
            year=self.year,
            start_date=date(self.year, 9, 14),
            end_date=date(self.year, 9, 14),
            stands_published=True,
        )
        self.company = Company.objects.create(name="Map company")
        self.client = Client(schema)

    def tearDown(self):
        cache.clear()
        self.media_override.disable()
        shutil.rmtree(self.media_root)

    def publish(self, preference, revision, name):
        release = StandMapRelease.objects.create(
            preference=preference, revision=revision
        )
        stand_map = StandMap.objects.create(
            release=release,
            date=preference.start_date,
            label="Day one",
            location="Realfagbygget",
            background=SimpleUploadedFile(
                name, b"not-used-by-model-validation", "image/png"
            ),
        )
        StandPlacement.objects.create(
            stand_map=stand_map,
            company=self.company,
            stand_number="A1",
            x_percent=Decimal("12.50"),
            y_percent=Decimal("34.25"),
        )
        return StandMapRelease.publish(release.pk, release.lock_version, self.user)

    def test_current_stand_map_is_null_without_current_published_release(self):
        old_preference = Preference.objects.create(
            active=False,
            year=self.year - 1,
            start_date=date(self.year - 1, 9, 14),
            end_date=date(self.year - 1, 9, 14),
        )
        self.publish(old_preference, 1, "old.png")
        StandMapRelease.objects.create(preference=self.preference, revision=1)

        executed = self.client.execute("{ currentStandMap { edition revision } }")

        self.assertIsNone(executed.get("errors"))
        self.assertIsNone(executed["data"]["currentStandMap"])

    def test_current_stand_map_returns_only_published_current_release(self):
        published = self.publish(self.preference, 1, "current.png")
        StandMapRelease.objects.create(preference=self.preference, revision=2)

        executed = self.client.execute(
            """
            {
              currentStandMap {
                edition
                revision
                maps {
                  date label location backgroundImage
                  placements { standNumber companyName companySlug xPercent yPercent }
                }
              }
            }
            """
        )

        self.assertIsNone(executed.get("errors"))
        result = executed["data"]["currentStandMap"]
        self.assertEqual(self.year, result["edition"])
        self.assertEqual(published.revision, result["revision"])
        self.assertEqual(
            self.preference.start_date.isoformat(), result["maps"][0]["date"]
        )
        self.assertEqual("Day one", result["maps"][0]["label"])
        self.assertEqual("Realfagbygget", result["maps"][0]["location"])
        self.assertEqual(
            reverse(
                "itdagene.stands.map_background",
                args=[published.maps.get().pk],
            ),
            result["maps"][0]["backgroundImage"],
        )
        self.assertEqual(
            {
                "standNumber": "A1",
                "companyName": "Map company",
                "companySlug": "map-company",
                "xPercent": 12.5,
                "yPercent": 34.25,
            },
            result["maps"][0]["placements"][0],
        )

    def test_visibility_setting_hides_an_existing_published_release(self):
        self.publish(self.preference, 1, "current.png")
        self.preference.stands_published = False
        self.preference.save()
        cache.clear()

        executed = self.client.execute(
            "{ currentMetaData { standsPublished } currentStandMap { edition } }"
        )

        self.assertIsNone(executed.get("errors"))
        self.assertFalse(executed["data"]["currentMetaData"]["standsPublished"])
        self.assertIsNone(executed["data"]["currentStandMap"])
