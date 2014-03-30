from django.test import TestCase

from django.core.urlresolvers import reverse


class UsersViewsTests(TestCase):
    def test_user_list_url_returns_right_view(self):
        response = self.client.get(reverse('users:list'))
        self.assertEqual(response.status_code, 200)
