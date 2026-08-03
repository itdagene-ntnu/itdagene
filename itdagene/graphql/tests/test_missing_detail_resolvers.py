from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from itdagene.graphql.query import Query


class TestMissingDetailResolvers(SimpleTestCase):
    @patch("itdagene.graphql.query.Stand.get_queryset")
    @patch("itdagene.graphql.query.Page.get_queryset")
    @patch("itdagene.graphql.query.Joblisting.get_queryset")
    def test_missing_details_return_none(
        self,
        get_joblistings: Mock,
        get_pages: Mock,
        get_stands: Mock,
    ) -> None:
        for get_queryset in (get_joblistings, get_pages, get_stands):
            get_queryset.return_value.filter.return_value.first.return_value = None

        query = Query()

        self.assertIsNone(query.resolve_joblisting(None, slug="missing-job"))
        self.assertIsNone(query.resolve_page(None, language="nb", slug="missing-page"))
        self.assertIsNone(query.resolve_stand(None, slug="missing-stand"))

        get_joblistings.return_value.filter.assert_called_once_with(slug="missing-job")
        get_pages.return_value.filter.assert_called_once_with(
            language="nb",
            slug="missing-page",
        )
        get_stands.return_value.filter.assert_called_once_with(slug="missing-stand")
