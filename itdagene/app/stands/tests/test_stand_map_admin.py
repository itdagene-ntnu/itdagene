import shutil
import tempfile
from datetime import date
from decimal import Decimal
from io import BytesIO
from unittest.mock import patch

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, transaction
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.timezone import now
from PIL import Image

from itdagene.app.company.models import Company
from itdagene.app.stands.forms import StandMapForm
from itdagene.app.stands.models import StandMap, StandMapRelease, StandPlacement
from itdagene.core.models import Preference, User


class TestStandMapAdmin(TestCase):
    def setUp(self):
        cache.clear()
        self.media_root = tempfile.mkdtemp()
        self.media_override = override_settings(MEDIA_ROOT=self.media_root)
        self.media_override.enable()
        self.user = User.objects.create(is_superuser=True, is_staff=True)
        year = now().year + 5
        self.preference = Preference.objects.create(
            active=True,
            year=year,
            start_date=date(year, 9, 14),
            end_date=date(year, 9, 14),
        )
        self.release = StandMapRelease.objects.create(
            preference=self.preference,
            revision=1,
        )

    def tearDown(self):
        cache.clear()
        self.media_override.disable()
        shutil.rmtree(self.media_root)

    def create_complete_draft(self):
        stand_map = StandMap.objects.create(
            release=self.release,
            date=self.preference.start_date,
            label="First day",
            location="Realfagbygget, U1",
            background=SimpleUploadedFile("map.png", b"model-test-image"),
        )
        company = Company.objects.create(name="Map company")
        placement = StandPlacement.objects.create(
            stand_map=stand_map,
            company=company,
            stand_number="A1",
            x_percent=Decimal("20.50"),
            y_percent=Decimal("30.25"),
        )
        return stand_map, placement

    def test_editor_requires_a_valid_raster_upload(self):
        form = StandMapForm(
            {"date": self.preference.start_date, "label": "Day one", "location": "A"},
            {"background": SimpleUploadedFile("map.txt", b"not an image")},
            instance=StandMap(release=self.release),
        )

        self.assertFalse(form.is_valid())
        self.assertIn("background", form.errors)

    def test_editor_rejects_disguised_and_decompression_bomb_images(self):
        image_bytes = BytesIO()
        Image.new("RGB", (1, 1)).save(image_bytes, format="GIF")
        disguised_form = StandMapForm(
            {"date": self.preference.start_date, "label": "Day one", "location": "A"},
            {
                "background": SimpleUploadedFile(
                    "map.png", image_bytes.getvalue(), content_type="image/png"
                )
            },
            instance=StandMap(release=self.release),
        )

        self.assertFalse(disguised_form.is_valid())
        self.assertIn("background", disguised_form.errors)

        bomb_form = StandMapForm(
            {"date": self.preference.start_date, "label": "Day one", "location": "A"},
            {"background": SimpleUploadedFile("map.png", b"image")},
            instance=StandMap(release=self.release),
        )
        with patch(
            "itdagene.app.stands.forms.Image.open",
            side_effect=Image.DecompressionBombError("too many pixels"),
        ):
            self.assertFalse(bomb_form.is_valid())
        self.assertIn("background", bomb_form.errors)

    def test_publish_requires_complete_draft(self):
        with self.assertRaises(ValidationError):
            StandMapRelease.publish(
                self.release.pk,
                self.release.lock_version,
                self.user,
            )

    def test_publish_requires_a_map_location(self):
        stand_map, _ = self.create_complete_draft()
        StandMap.objects.filter(pk=stand_map.pk).update(location="")

        with self.assertRaises(ValidationError):
            StandMapRelease.publish(
                self.release.pk,
                self.release.lock_version,
                self.user,
            )

    def test_published_map_and_placements_cannot_be_created_or_changed(self):
        stand_map, placement = self.create_complete_draft()
        StandMapRelease.publish(
            self.release.pk,
            self.release.lock_version,
            self.user,
        )

        with self.assertRaises(ValidationError):
            StandMap.objects.create(
                release=self.release,
                date=self.preference.start_date,
                background=SimpleUploadedFile("another.png", b"not-used"),
            )
        with self.assertRaises(ValidationError):
            placement.x_percent = Decimal("30")
            placement.save()
        with self.assertRaises(ValidationError):
            placement.delete()
        with self.assertRaises(ValidationError):
            stand_map.delete()
        with self.assertRaises(ValidationError):
            self.release.delete()

    def test_editor_uses_css_safe_decimal_coordinates(self):
        self.create_complete_draft()
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("itdagene.stand_maps.edit", args=[self.release.pk])
        )

        self.assertEqual(200, response.status_code)
        self.assertContains(response, "left: 20.50%; top: 30.25%;")

    def test_new_draft_clones_the_published_release(self):
        source_map, source_placement = self.create_complete_draft()
        StandMapRelease.publish(
            self.release.pk,
            self.release.lock_version,
            self.user,
        )
        self.client.force_login(self.user)

        response = self.client.post(reverse("itdagene.stand_maps.create"))

        self.assertEqual(302, response.status_code)
        draft = StandMapRelease.objects.get(
            preference=self.preference,
            revision=self.release.revision + 1,
        )
        cloned_map = draft.maps.get()
        cloned_placement = cloned_map.placements.get()
        self.assertEqual(source_map.background.name, cloned_map.background.name)
        self.assertEqual(source_placement.company_id, cloned_placement.company_id)
        self.assertEqual(source_placement.company_name, cloned_placement.company_name)
        self.assertEqual(source_placement.x_percent, cloned_placement.x_percent)

    def test_stale_lock_version_cannot_publish(self):
        self.create_complete_draft()

        with self.assertRaises(ValidationError):
            StandMapRelease.publish(
                self.release.pk,
                self.release.lock_version + 1,
                self.user,
            )

    def test_only_one_release_can_be_published_for_an_edition(self):
        self.create_complete_draft()
        StandMapRelease.publish(
            self.release.pk,
            self.release.lock_version,
            self.user,
        )
        second = StandMapRelease.objects.create(
            preference=self.preference,
            revision=2,
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                StandMapRelease.objects.filter(pk=second.pk).update(
                    status=StandMapRelease.PUBLISHED
                )

    def test_company_slugs_are_unique_within_a_map(self):
        stand_map, first = self.create_complete_draft()
        second_company = Company.objects.create(name="Map-company")
        second = StandPlacement.objects.create(
            stand_map=stand_map,
            company=second_company,
            stand_number="A2",
            x_percent=Decimal("40"),
            y_percent=Decimal("50"),
        )

        self.assertEqual("map-company", first.company_slug)
        self.assertEqual(
            "map-company-{}".format(second_company.pk),
            second.company_slug,
        )

    def test_only_published_current_backgrounds_are_public(self):
        stand_map, _ = self.create_complete_draft()
        background_url = reverse(
            "itdagene.stands.map_background",
            args=[stand_map.pk],
        )

        self.assertEqual(404, self.client.get(background_url).status_code)
        StandMapRelease.publish(
            self.release.pk,
            self.release.lock_version,
            self.user,
        )

        response = self.client.get(background_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            "public, max-age=31536000, immutable",
            response["Cache-Control"],
        )

    def test_staff_can_open_the_editor_and_publish_is_post_only(self):
        self.client.force_login(self.user)

        self.assertEqual(
            200, self.client.get(reverse("itdagene.stand_maps.list")).status_code
        )
        self.assertEqual(
            405,
            self.client.get(
                reverse("itdagene.stand_maps.publish", args=[self.release.pk])
            ).status_code,
        )
