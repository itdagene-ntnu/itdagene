from datetime import date

from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.test import RequestFactory, TestCase

from itdagene.core.models import Preference, User
from itdagene.core.views import error403, error404, error500


class TestErrorStatuses(TestCase):
    def setUp(self):
        cache.clear()
        User.objects.create(is_superuser=True)
        Preference.objects.create(
            active=True,
            year=2031,
            start_date=date(2031, 9, 14),
            end_date=date(2031, 9, 15),
        )
        self.request = RequestFactory().get("/missing/")
        self.request.user = AnonymousUser()

    def tearDown(self):
        cache.clear()

    def test_error_pages_preserve_their_http_statuses(self):
        self.assertEqual(403, error403(self.request, Exception()).status_code)
        self.assertEqual(404, error404(self.request, Exception()).status_code)
        self.assertEqual(500, error500(self.request).status_code)
