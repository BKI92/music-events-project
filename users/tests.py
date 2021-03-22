from django.shortcuts import get_object_or_404
from django.test import TestCase, Client
from rest_framework import status

from api.models import User


class UserTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url_registration = '/api/v1/user/registration/'
        self.url_token = '/api/v1/user/token/'
        self.user = User.objects.create_user(
            username="sarah", email="connor.s@skynet.com",
            password="12345qwerty"
        )
        self.client.login(username=self.user.username,
                          password=self.user.password)

    def test_registration_ok(self):
        """Тест успешной регистрации"""
        response = self.client.post(self.url_registration,
                                    {'username': 'Vasya',
                                     'password': 'admin1234'})
        user = get_object_or_404(User, username='Vasya')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.username, 'Vasya')

    def test_registration_false(self):
        """Тест неуспешной регистрации."""
        response = self.client.post('/api/v1/user/registration/',
                                    {'username': self.user.username,
                                     'password': self.user.password})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         'Пользователь уже существует.')
        response1 = self.client.post('/api/v1/user/registration/',
                                     {'username': '',
                                      'password': self.user.password})
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST,
                         'username не может состоять из пробельного символа.')
        response2 = self.client.post('/api/v1/user/registration/',
                                     {'username': 'Robinson2',
                                      'password': ''})
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST,
                         'Пароль не может быть пробельным символом.')
        response3 = self.client.post('/api/v1/user/registration/',
                                     {'username': 'Robinson3'})
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST,
                         'Не передали пароль.')



