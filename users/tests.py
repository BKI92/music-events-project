from django.shortcuts import get_object_or_404
from django.test import TestCase, Client
from rest_framework import status

from api.models import User


class ApiTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url_registration = '/api/v1/user/registration/'
        self.user = User.objects.create_user(
            username="sarah", email="connor.s@skynet.com",
            password="12345qwerty"
        )
        self.client.login(username=self.user.username,
                          password=self.user.password)

    def test_registration(self):
        self.client.post(self.url_registration, {'username': 'Vasya',
                                                 'password': 'admin1234'})
        user = get_object_or_404(User, username='Vasya')
        self.assertEqual(user.username, 'Vasya')

    def test_registration_2(self):
        response = self.client.post('/api/v1/user/registration/',
                                    {'username': self.user.username,
                                     'password': self.user.password})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
