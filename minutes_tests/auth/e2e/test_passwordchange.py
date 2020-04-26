from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from rest_framework.test import APIClient

from minutes.auth.models import Token, TokenTypes

INITIAL_PASSWORD = 'initialpassword'
CHANGED_PASSWORD = 'changedpassword'


class PasswordChangeTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(username='testuser')
        self.user.set_password(INITIAL_PASSWORD)
        self.user.save()
        self.user_token = Token.objects.create(user=self.user, token_type=TokenTypes.AUTH)

    def test_401_if_not_authenticated(self):
        response = self.client.post('/api/v1/changepassword/', {})
        self.assertEqual(response.status_code, 401)

    def test_400_if_not_providing_old_password(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.post('/api/v1/changepassword/', {'new_password': CHANGED_PASSWORD})
        self.assertEqual(response.status_code, 400)

    def test_403_if_providing_wrong_old_password(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.post(
            '/api/v1/changepassword/',
            {'old_password': 'notcorrect', 'new_password': CHANGED_PASSWORD}
        )
        self.assertEqual(response.status_code, 403)

    def test_201_for_correct_change_request_and_verify_new_password(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.post(
            '/api/v1/changepassword/',
            {'old_password': INITIAL_PASSWORD, 'new_password': CHANGED_PASSWORD}
        )
        self.assertEqual(response.status_code, 204)
        response = self.client.post(
            '/api/v1/token/',
            {'username': self.user.username, 'password': INITIAL_PASSWORD}
        )
        self.assertEqual(response.status_code, 400)
        response = self.client.post(
            '/api/v1/token/',
            {'username': self.user.username, 'password': CHANGED_PASSWORD}
        )
        self.assertEqual(response.status_code, 201)

