from django.urls import reverse
from django.test import TestCase

from backend.consts import HttpStatus


class AccountsTest(TestCase):
    fixtures = [
        'resources/tests/accounts/users.json',
    ]

    @classmethod
    def setUpClass(cls):
        cls.logout_url = reverse('accounts:logout')
        super().setUpClass()

    def test_logout_on_get(self):
        logged = self.client.login(username='admin', password='password')
        self.assertTrue(logged)
        response = self.client.get(self.logout_url, follow=True)

        self.assertEqual(response.status_code, HttpStatus.OK)
        context = response.context
        self.assertFalse(context['user'].is_authenticated)

    def test_logout_on_post(self):
        logged = self.client.login(username='admin', password='password')
        self.assertTrue(logged)
        response = self.client.post(self.logout_url, data={}, follow=True)

        self.assertEqual(response.status_code, HttpStatus.OK)
        context = response.context
        self.assertFalse(context['user'].is_authenticated)
