from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from itdagene.app.company.models import Company
from itdagene.graphql.object_types import MetaData


class TestPartnerVisibility(SimpleTestCase):
    @patch.object(Company, "get_main_collaborator")
    def test_main_collaborator_respects_admin_visibility(
        self,
        get_main_collaborator: Mock,
    ) -> None:
        partner = object()
        get_main_collaborator.return_value = partner

        hidden_metadata = SimpleNamespace(view_hsp=False)
        visible_metadata = SimpleNamespace(view_hsp=True)

        self.assertIsNone(
            MetaData.resolve_main_collaborator(hidden_metadata, info=None)
        )
        get_main_collaborator.assert_not_called()

        self.assertIs(
            MetaData.resolve_main_collaborator(visible_metadata, info=None),
            partner,
        )
        get_main_collaborator.assert_called_once_with()

    @patch.object(Company, "get_collaborators")
    def test_collaborators_respect_admin_visibility(
        self,
        get_collaborators: Mock,
    ) -> None:
        partners = [object()]
        get_collaborators.return_value = partners

        hidden_metadata = SimpleNamespace(view_sp=False)
        visible_metadata = SimpleNamespace(view_sp=True)

        self.assertIsNone(MetaData.resolve_collaborators(hidden_metadata, info=None))
        get_collaborators.assert_not_called()

        self.assertIs(
            MetaData.resolve_collaborators(visible_metadata, info=None),
            partners,
        )
        get_collaborators.assert_called_once_with()

    @patch.object(Company, "get_last_day")
    @patch.object(Company, "get_first_day")
    def test_company_lists_respect_admin_visibility(
        self,
        get_first_day: Mock,
        get_last_day: Mock,
    ) -> None:
        first_day_companies = [object()]
        last_day_companies = [object()]
        get_first_day.return_value = first_day_companies
        get_last_day.return_value = last_day_companies

        hidden_metadata = SimpleNamespace(view_companies=False)
        visible_metadata = SimpleNamespace(view_companies=True)

        self.assertIsNone(
            MetaData.resolve_companies_first_day(hidden_metadata, info=None)
        )
        self.assertIsNone(
            MetaData.resolve_companies_last_day(hidden_metadata, info=None)
        )
        get_first_day.assert_not_called()
        get_last_day.assert_not_called()

        self.assertIs(
            MetaData.resolve_companies_first_day(visible_metadata, info=None),
            first_day_companies,
        )
        self.assertIs(
            MetaData.resolve_companies_last_day(visible_metadata, info=None),
            last_day_companies,
        )
        get_first_day.assert_called_once_with()
        get_last_day.assert_called_once_with()
