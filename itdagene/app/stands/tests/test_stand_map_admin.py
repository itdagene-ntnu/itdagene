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

from itdagene.app.company import COMPANY_STATUS_SIGNED
from itdagene.app.company.models import Company, Package
from itdagene.app.stands.forms import StandMapForm, StandPlacementForm
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

    def valid_png_upload(self, name="map.png", color="blue"):
        image_bytes = BytesIO()
        Image.new("RGB", (4, 4), color=color).save(image_bytes, format="PNG")
        return SimpleUploadedFile(
            name,
            image_bytes.getvalue(),
            content_type="image/png",
        )

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

    def test_upload_for_an_existing_day_replaces_that_maps_background(self):
        stand_map, _ = self.create_complete_draft()
        original_background = stand_map.background.name
        original_lock_version = self.release.lock_version
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("itdagene.stand_maps.edit", args=[self.release.pk]),
            {
                "action": "save-map",
                "lock_version": original_lock_version,
                "date": self.preference.start_date,
                "label": "Oppdatert messedag",
                "location": "Realfagbygget, U1",
                "background": self.valid_png_upload("replacement.png", "green"),
            },
        )

        self.assertEqual(302, response.status_code)
        self.assertEqual(1, self.release.maps.count())
        stand_map.refresh_from_db()
        self.release.refresh_from_db()
        self.assertEqual("Oppdatert messedag", stand_map.label)
        self.assertNotEqual(original_background, stand_map.background.name)
        self.assertIn("replacement", stand_map.background.name)
        self.assertEqual(original_lock_version + 1, self.release.lock_version)

    def test_duplicate_placement_returns_the_correct_conflict_message(self):
        stand_map, existing_placement = self.create_complete_draft()
        package = Package.objects.create(
            name="Duplicate placement package",
            description="",
            price=0,
        )
        company = Company.objects.create(
            name="Another map company",
            package=package,
            status=COMPANY_STATUS_SIGNED,
        )
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("itdagene.stand_maps.edit", args=[self.release.pk]),
            {
                "action": "save-placement",
                "map_id": stand_map.pk,
                "lock_version": self.release.lock_version,
                "new-placement-{}-company".format(stand_map.pk): company.pk,
                "new-placement-{}-stand_number".format(
                    stand_map.pk
                ): existing_placement.stand_number,
                "new-placement-{}-x_percent".format(stand_map.pk): "40.00",
                "new-placement-{}-y_percent".format(stand_map.pk): "50.00",
            },
            follow=True,
        )

        self.assertEqual(200, response.status_code)
        self.assertContains(
            response,
            "bedriften eller standnummeret allerede er brukt på dette kartet",
        )
        self.assertEqual(1, stand_map.placements.count())

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
        stand_map, _ = self.create_complete_draft()
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("itdagene.stand_maps.edit", args=[self.release.pk])
        )

        self.assertEqual(200, response.status_code)
        self.assertContains(response, "left: 20.50%; top: 30.25%;")
        self.assertContains(
            response,
            'data-new-placement-popover="new-placement-popover-{}"'.format(
                stand_map.pk
            ),
        )
        self.assertContains(
            response,
            'id="new-placement-form-{}"'.format(stand_map.pk),
        )
        self.assertContains(response, 'data-marker-placement="')
        self.assertContains(response, "Klikk i kartet for å plassere en ny stand.")
        self.assertContains(
            response,
            "Flytt markøren eller endre koordinatene, og lagre plasseringen.",
        )
        self.assertContains(response, "marker.setPointerCapture(pointerId)")
        self.assertContains(response, 'marker.dataset.dragging = "true"')
        self.assertContains(
            response,
            "function coordinatesFor(canvas, event) {",
            count=1,
        )
        self.assertContains(response, 'canvas.dataset.placing = "true"')
        self.assertContains(response, "function positionPopover(")
        self.assertContains(response, "function openPlacement(")
        self.assertContains(response, "position: fixed")
        self.assertContains(response, "window.visualViewport")
        self.assertContains(response, "window.requestAnimationFrame")
        self.assertContains(response, 'window.addEventListener("scroll"')
        self.assertContains(response, "data-placement-popover")
        self.assertContains(response, "Legg til og fortsett")
        self.assertContains(response, "Plasser med koordinater")
        self.assertContains(response, "var x = rawX ? Number(")
        self.assertContains(response, 'event.key !== "Escape"')
        self.assertContains(response, "form.requestSubmit")
        self.assertNotContains(response, "new-placement-details-")
        self.assertContains(
            response,
            ".stand-map-marker:not(.stand-map-marker--preview)",
        )
        self.assertContains(response, ".stand-map-marker--preview::before")
        self.assertContains(response, "place-items: center")

    def test_draft_editor_explains_public_placeholder_and_publish_action(self):
        self.create_complete_draft()
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("itdagene.stand_maps.edit", args=[self.release.pk])
        )

        self.assertContains(response, "Offentlig nettside: plassholderen vises")
        self.assertContains(response, "Vis stands er slått av")
        self.assertContains(response, "Publiser versjon")
        self.assertNotContains(response, "Publiser og vis kartet")

    def test_editor_explains_enabled_setting_without_a_published_release(self):
        self.preference.stands_published = True
        self.preference.save()
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("itdagene.stand_maps.edit", args=[self.release.pk])
        )

        self.assertContains(response, "Offentlig nettside: plassholderen vises")
        self.assertContains(response, "Ingen standkartversjon er publisert ennå")

    def test_published_editor_distinguishes_release_from_visibility_setting(self):
        self.create_complete_draft()
        StandMapRelease.publish(
            self.release.pk,
            self.release.lock_version,
            self.user,
        )
        self.client.force_login(self.user)

        hidden_response = self.client.get(
            reverse("itdagene.stand_maps.edit", args=[self.release.pk])
        )
        self.assertContains(hidden_response, "Vis stands er slått av")
        self.assertNotContains(
            hidden_response,
            "Offentlig nettside: denne versjonen vises",
        )

        self.preference.stands_published = True
        self.preference.save()
        cache.clear()
        visible_response = self.client.get(
            reverse("itdagene.stand_maps.edit", args=[self.release.pk])
        )
        self.assertContains(
            visible_response,
            "Offentlig nettside: denne versjonen vises",
        )

    def test_placement_forms_have_unique_ids_and_native_company_search(self):
        stand_map, placement = self.create_complete_draft()
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("itdagene.stand_maps.edit", args=[self.release.pk])
        )

        self.assertContains(
            response,
            'id="id_placement-{}-company"'.format(placement.pk),
            count=1,
        )
        self.assertContains(
            response,
            'id="id_new-placement-{}-company"'.format(stand_map.pk),
            count=1,
        )
        self.assertNotContains(response, 'id="id_company"')
        self.assertContains(response, 'type="search"')
        self.assertContains(response, "data-company-filter")
        self.assertContains(
            response,
            'aria-controls="id_new-placement-{}-company"'.format(stand_map.pk),
        )
        self.assertContains(response, "er valgt.")
        self.assertNotContains(response, 'trigger("chosen:activate")')

    def test_next_stand_number_uses_the_first_available_positive_integer(self):
        stand_map, _ = self.create_complete_draft()
        first_company = Company.objects.create(name="First numeric company")
        third_company = Company.objects.create(name="Third numeric company")
        StandPlacement.objects.create(
            stand_map=stand_map,
            company=first_company,
            stand_number="1",
            x_percent=Decimal("40"),
            y_percent=Decimal("50"),
        )
        StandPlacement.objects.create(
            stand_map=stand_map,
            company=third_company,
            stand_number="3",
            x_percent=Decimal("60"),
            y_percent=Decimal("70"),
        )

        self.assertEqual("2", StandPlacement.next_available_number(stand_map))

    def test_placement_form_uses_norwegian_labels_and_searchable_company(self):
        form = StandPlacementForm()

        self.assertEqual("Bedrift", form.fields["company"].label)
        self.assertEqual("Standnummer", form.fields["stand_number"].label)
        self.assertEqual(
            "company",
            form.fields["company"].widget.attrs["data-stand-field"],
        )
        self.assertEqual(
            "x_percent",
            form.fields["x_percent"].widget.attrs["data-stand-field"],
        )

    def test_placement_form_lists_active_companies_before_signing(self):
        self.create_complete_draft()
        contacted_company = Company.objects.create(
            name="Contacted without package",
            status=4,
        )
        inactive_company = Company.objects.create(
            name="Inactive company",
            active=False,
        )

        queryset = StandPlacementForm().fields["company"].queryset

        self.assertTrue(queryset.filter(pk=contacted_company.pk).exists())
        self.assertFalse(queryset.filter(pk=inactive_company.pk).exists())

        self.client.force_login(self.user)
        response = self.client.get(
            reverse("itdagene.stand_maps.edit", args=[self.release.pk])
        )

        self.assertContains(
            response,
            '<option value="{}">Contacted without package</option>'.format(
                contacted_company.pk
            ),
            html=True,
        )
        self.assertNotContains(
            response,
            '<option value="{}">Inactive company</option>'.format(inactive_company.pk),
            html=True,
        )

    def test_placement_form_keeps_an_assigned_company_after_deactivation(self):
        _stand_map, placement = self.create_complete_draft()
        Company.objects.filter(pk=placement.company_id).update(active=False)

        queryset = StandPlacementForm(instance=placement).fields["company"].queryset

        self.assertTrue(queryset.filter(pk=placement.company_id).exists())

    def test_successful_new_placement_advances_the_suggested_number(self):
        stand_map, _ = self.create_complete_draft()
        package = Package.objects.create(
            name="Sequential package",
            description="",
            price=0,
        )
        company = Company.objects.create(
            name="Sequential company",
            package=package,
            status=COMPANY_STATUS_SIGNED,
        )
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("itdagene.stand_maps.edit", args=[self.release.pk]),
            {
                "action": "save-placement",
                "map_id": stand_map.pk,
                "lock_version": self.release.lock_version,
                "new-placement-{}-company".format(stand_map.pk): company.pk,
                "new-placement-{}-stand_number".format(stand_map.pk): "1",
                "new-placement-{}-x_percent".format(stand_map.pk): "45.00",
                "new-placement-{}-y_percent".format(stand_map.pk): "55.00",
            },
        )

        self.assertEqual(302, response.status_code)
        self.assertEqual(
            "{}#stand-map-{}".format(
                reverse("itdagene.stand_maps.edit", args=[self.release.pk]),
                stand_map.pk,
            ),
            response["Location"],
        )
        response = self.client.get(
            reverse("itdagene.stand_maps.edit", args=[self.release.pk])
        )
        self.assertEqual(
            "2",
            response.context["editor_maps"][0]["new_placement_form"][
                "stand_number"
            ].value(),
        )

    def test_new_placement_number_is_scoped_to_each_map(self):
        first_map, _ = self.create_complete_draft()
        self.preference.end_date = date(self.preference.year, 9, 15)
        self.preference.save()
        second_map = StandMap.objects.create(
            release=self.release,
            date=self.preference.end_date,
            label="Second day",
            location="Realfagbygget, U1",
            background=SimpleUploadedFile("second-map.png", b"second-map-image"),
        )
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("itdagene.stand_maps.edit", args=[self.release.pk])
        )

        forms_by_map = {
            item["stand_map"].pk: item["new_placement_form"]
            for item in response.context["editor_maps"]
        }
        self.assertEqual("1", forms_by_map[first_map.pk]["stand_number"].value())
        self.assertEqual("1", forms_by_map[second_map.pk]["stand_number"].value())

    def test_draft_editor_persists_changed_placement_coordinates(self):
        stand_map, placement = self.create_complete_draft()
        package = Package.objects.create(
            name="Map package",
            description="",
            price=0,
        )
        Company.objects.filter(pk=placement.company_id).update(
            package=package,
            status=COMPANY_STATUS_SIGNED,
        )
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("itdagene.stand_maps.edit", args=[self.release.pk]),
            {
                "action": "save-placement",
                "map_id": stand_map.pk,
                "placement_id": placement.pk,
                "lock_version": self.release.lock_version,
                "placement-{}-company".format(placement.pk): placement.company_id,
                "placement-{}-stand_number".format(
                    placement.pk
                ): placement.stand_number,
                "placement-{}-x_percent".format(placement.pk): "72.50",
                "placement-{}-y_percent".format(placement.pk): "67.00",
            },
        )

        self.assertRedirects(
            response,
            "{}#stand-map-{}".format(
                reverse("itdagene.stand_maps.edit", args=[self.release.pk]),
                stand_map.pk,
            ),
        )
        placement.refresh_from_db()
        self.assertEqual(Decimal("72.50"), placement.x_percent)
        self.assertEqual(Decimal("67.00"), placement.y_percent)

    def test_published_editor_is_read_only_and_offers_an_editable_draft(self):
        self.create_complete_draft()
        StandMapRelease.publish(
            self.release.pk,
            self.release.lock_version,
            self.user,
        )
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("itdagene.stand_maps.edit", args=[self.release.pk])
        )

        self.assertContains(response, "Opprett redigerbar kladd")
        self.assertContains(response, 'class="stand-map-readonly"')
        self.assertNotContains(response, 'name="placement-')
        self.assertNotContains(response, 'name="new-placement-')

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

        self.assertFalse(Preference.objects.get(pk=self.preference.pk).stands_published)
        self.assertEqual(404, self.client.get(background_url).status_code)

        self.preference.stands_published = True
        self.preference.save()
        cache.clear()
        response = self.client.get(background_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            "no-store, max-age=0",
            response["Cache-Control"],
        )
        self.assertEqual("no-cache", response["Pragma"])

        self.preference.stands_published = False
        self.preference.save()
        cache.clear()
        self.assertEqual(404, self.client.get(background_url).status_code)

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
