from datetime import date

from django.core.cache import cache
from django.test import TestCase
from graphene.test import Client

from itdagene.app.company import COMPANY_STATUS_INTERESTED, COMPANY_STATUS_SIGNED
from itdagene.app.company.models import Company, Package
from itdagene.core.models import Preference, User
from itdagene.graphql.schema import schema


class TestCompanyPublication(TestCase):
    query = """
        {
          currentMetaData {
            companiesFirstDay { name logo(width: 320, height: 120) }
            companiesLastDay { name logo(width: 320, height: 120) }
            collaborators { name }
            mainCollaborator { name }
          }
        }
    """

    def setUp(self) -> None:
        cache.clear()
        User.objects.create(is_superuser=True)
        self.preference = Preference.objects.create(
            active=True,
            year=2031,
            start_date=date(2031, 9, 14),
            end_date=date(2031, 9, 15),
        )
        self.client = Client(schema)

    def tearDown(self) -> None:
        cache.clear()

    def create_package(
        self,
        name: str,
        *,
        first_day: bool = False,
        last_day: bool = False,
    ) -> Package:
        return Package.objects.create(
            name=name,
            description=f"Package for {name}",
            price=1,
            has_stand_first_day=first_day,
            has_stand_last_day=last_day,
        )

    def create_company(
        self,
        name: str,
        package: Package,
        *,
        active: bool = True,
        status: int = COMPANY_STATUS_SIGNED,
    ) -> Company:
        return Company.objects.create(
            active=active,
            name=name,
            package=package,
            status=status,
        )

    def execute(self) -> dict:
        executed = self.client.execute(self.query)
        self.assertIsNone(executed.get("errors"))
        return executed["data"]["currentMetaData"]

    def test_hidden_company_lists_are_null_and_published_empty_lists_are_empty(
        self,
    ) -> None:
        hidden = self.execute()

        self.assertIsNone(hidden["companiesFirstDay"])
        self.assertIsNone(hidden["companiesLastDay"])

        self.preference.view_companies = True
        self.preference.save()
        published = self.execute()

        self.assertEqual([], published["companiesFirstDay"])
        self.assertEqual([], published["companiesLastDay"])

    def test_published_days_include_active_signed_companies_without_logos(
        self,
    ) -> None:
        package = self.create_package(
            "Stand",
            first_day=True,
            last_day=True,
        )
        self.create_company("Visible without logo", package)
        self.create_company(
            "Not signed",
            package,
            status=COMPANY_STATUS_INTERESTED,
        )
        self.create_company("Inactive", package, active=False)
        self.preference.view_companies = True
        self.preference.save()

        published = self.execute()
        expected = [{"name": "Visible without logo", "logo": None}]

        self.assertEqual(expected, published["companiesFirstDay"])
        self.assertEqual(expected, published["companiesLastDay"])

    def test_partner_tiers_only_include_active_signed_companies(self) -> None:
        collaborator_package = self.create_package("Samarbeidspartner")
        main_package = self.create_package("Hovedsamarbeidspartner")
        self.create_company("Visible collaborator", collaborator_package)
        self.create_company(
            "Unsigned collaborator",
            collaborator_package,
            status=COMPANY_STATUS_INTERESTED,
        )
        self.create_company(
            "Inactive collaborator",
            collaborator_package,
            active=False,
        )
        self.create_company("Visible main partner", main_package)
        self.create_company(
            "Unsigned main partner",
            main_package,
            status=COMPANY_STATUS_INTERESTED,
        )
        self.preference.view_sp = True
        self.preference.view_hsp = True
        self.preference.save()

        published = self.execute()

        self.assertEqual(
            [{"name": "Visible collaborator"}],
            published["collaborators"],
        )
        self.assertEqual(
            {"name": "Visible main partner"},
            published["mainCollaborator"],
        )
