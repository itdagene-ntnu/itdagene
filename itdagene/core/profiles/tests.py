from django.contrib.auth.models import User
from django.test import TestCase


class ModelTest(TestCase):
    def test_that_new_users_also_have_a_profile(self):
        user = User.objects.create_user('adrian', 'adrian@example.com')

        self.assertEqual(user.id, user.profile.user.id)
