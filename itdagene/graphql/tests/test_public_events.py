from datetime import date, time
from typing import Optional

from django.core.cache import cache
from django.test import TestCase
from django.utils.timezone import now
from graphene.test import Client
from graphql_relay import to_global_id

from itdagene.app.company import COMPANY_STATUS_SIGNED
from itdagene.app.company.models import Company, Package
from itdagene.app.events.models import Event
from itdagene.app.stands.models import DigitalStand
from itdagene.core.models import Preference, User
from itdagene.graphql.schema import schema


class TestPublicEvents(TestCase):
    def setUp(self) -> None:
        cache.clear()
        User.objects.create(is_superuser=True)

        self.edition_year = now().year + 5
        self.preference = Preference.objects.create(
            active=True,
            year=self.edition_year,
            start_date=date(self.edition_year, 9, 14),
            end_date=date(self.edition_year, 9, 15),
            program_published=True,
        )
        package = Package.objects.create(
            name="Stand package",
            description="Includes a stand",
            price=1,
            has_stand_first_day=True,
            has_stand_last_day=True,
        )
        self.company = Company.objects.create(
            name="Public company",
            package=package,
            status=COMPANY_STATUS_SIGNED,
        )
        self.stand = DigitalStand.objects.create(
            active=True,
            company=self.company,
            slug="public-company",
        )
        self.client = Client(schema)

    def tearDown(self) -> None:
        cache.clear()

    def create_event(
        self,
        title: str,
        *,
        event_date: Optional[date] = None,
        year: Optional[int] = None,
        event_type: int = 0,
        internal: bool = False,
        stand: Optional[DigitalStand] = None,
    ) -> Event:
        event_year = year if year is not None else self.edition_year
        return Event.objects.create(
            title=title,
            date=event_date or date(event_year, 9, 14),
            time_start=time(9, 0),
            time_end=time(10, 0),
            description=f"Description for {title}",
            type=event_type,
            location="U1",
            is_internal=internal,
            stand=stand,
        )

    def test_root_events_only_exposes_public_active_edition_program(self) -> None:
        current_event = self.create_event("Current program event")
        promoted_stand_event = self.create_event(
            "Promoted stand event",
            event_type=7,
            stand=self.stand,
        )
        self.create_event("Internal event", internal=True)
        self.create_event("Ordinary stand event", stand=self.stand)
        self.create_event("Previous edition", year=self.edition_year - 1)
        self.create_event("Calendar-year event", year=now().year)

        executed = self.client.execute(
            """
            {
              events {
                id
                title
              }
            }
            """
        )

        self.assertIsNone(executed.get("errors"))
        self.assertCountEqual(
            [
                {
                    "id": to_global_id("Event", current_event.pk),
                    "title": current_event.title,
                },
                {
                    "id": to_global_id("Event", promoted_stand_event.pk),
                    "title": promoted_stand_event.title,
                },
            ],
            executed["data"]["events"],
        )

    def test_public_program_can_include_dates_outside_the_fair_period(self) -> None:
        before_fair = self.create_event(
            "Before the event",
            event_date=date(self.edition_year, 9, 13),
        )
        first_day = self.create_event(
            "First event day",
            event_date=self.preference.start_date,
        )
        last_day = self.create_event(
            "Last event day",
            event_date=self.preference.end_date,
        )
        after_fair = self.create_event(
            "After the event",
            event_date=date(self.edition_year, 9, 16),
        )

        executed = self.client.execute("{ events { id title } }")

        self.assertIsNone(executed.get("errors"))
        self.assertCountEqual(
            [
                {
                    "id": to_global_id("Event", before_fair.pk),
                    "title": before_fair.title,
                },
                {
                    "id": to_global_id("Event", first_day.pk),
                    "title": first_day.title,
                },
                {
                    "id": to_global_id("Event", last_day.pk),
                    "title": last_day.title,
                },
                {
                    "id": to_global_id("Event", after_fair.pk),
                    "title": after_fair.title,
                },
            ],
            executed["data"]["events"],
        )

    def test_stand_events_only_exposes_public_active_edition_events(self) -> None:
        ordinary_event = self.create_event("Ordinary stand event", stand=self.stand)
        promoted_event = self.create_event(
            "Promoted stand event",
            event_type=7,
            stand=self.stand,
        )
        self.create_event("Internal stand event", internal=True, stand=self.stand)
        self.create_event(
            "Previous stand event",
            year=self.edition_year - 1,
            stand=self.stand,
        )

        executed = self.client.execute(
            """
            query ($slug: String!) {
              stand(slug: $slug) {
                events {
                  id
                  title
                }
              }
            }
            """,
            variable_values={"slug": self.stand.slug},
        )

        self.assertIsNone(executed.get("errors"))
        self.assertCountEqual(
            [
                {
                    "id": to_global_id("Event", ordinary_event.pk),
                    "title": ordinary_event.title,
                },
                {
                    "id": to_global_id("Event", promoted_event.pk),
                    "title": promoted_event.title,
                },
            ],
            executed["data"]["stand"]["events"],
        )

    def test_relay_node_enforces_public_event_policy(self) -> None:
        public_stand_event = self.create_event(
            "Public stand event",
            stand=self.stand,
        )
        internal_event = self.create_event("Internal event", internal=True)

        query = """
            query ($id: ID!) {
              node(id: $id) {
                __typename
                ... on Event {
                  id
                  title
                }
              }
            }
        """
        public_id = to_global_id("Event", public_stand_event.pk)
        public_result = self.client.execute(
            query,
            variable_values={"id": public_id},
        )
        internal_result = self.client.execute(
            query,
            variable_values={"id": to_global_id("Event", internal_event.pk)},
        )

        self.assertIsNone(public_result.get("errors"))
        self.assertEqual(
            {
                "__typename": "Event",
                "id": public_id,
                "title": public_stand_event.title,
            },
            public_result["data"]["node"],
        )
        self.assertIsNone(internal_result.get("errors"))
        self.assertIsNone(internal_result["data"]["node"])

    def test_relay_nodes_enforce_public_event_policy(self) -> None:
        public_event = self.create_event("Public event")
        public_stand_event = self.create_event(
            "Public stand event",
            stand=self.stand,
        )
        internal_event = self.create_event("Internal event", internal=True)
        previous_event = self.create_event(
            "Previous event",
            year=self.edition_year - 1,
        )
        ids = [
            to_global_id("Event", event.pk)
            for event in (
                public_event,
                public_stand_event,
                internal_event,
                previous_event,
            )
        ]

        executed = self.client.execute(
            """
            query ($ids: [ID!]!) {
              nodes(ids: $ids) {
                __typename
                ... on Event {
                  id
                  title
                }
              }
            }
            """,
            variable_values={"ids": ids},
        )

        self.assertIsNone(executed.get("errors"))
        self.assertEqual(
            [
                {
                    "__typename": "Event",
                    "id": ids[0],
                    "title": public_event.title,
                },
                {
                    "__typename": "Event",
                    "id": ids[1],
                    "title": public_stand_event.title,
                },
                None,
                None,
            ],
            executed["data"]["nodes"],
        )

    def test_unpublished_program_is_hidden_from_every_event_entry_point(self) -> None:
        event = self.create_event("Hidden program event", stand=self.stand)
        self.preference.program_published = False
        self.preference.save()
        cache.clear()

        executed = self.client.execute(
            """
            query ($node: ID!, $nodes: [ID!]!, $slug: String!) {
              events { id }
              stand(slug: $slug) { events { id } }
              node(id: $node) { id }
              nodes(ids: $nodes) { id }
            }
            """,
            variable_values={
                "node": to_global_id("Event", event.pk),
                "nodes": [to_global_id("Event", event.pk)],
                "slug": self.stand.slug,
            },
        )

        self.assertIsNone(executed.get("errors"))
        self.assertEqual([], executed["data"]["events"])
        self.assertEqual([], executed["data"]["stand"]["events"])
        self.assertIsNone(executed["data"]["node"])
        self.assertEqual([None], executed["data"]["nodes"])
