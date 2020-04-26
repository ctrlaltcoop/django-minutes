from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from rest_framework.test import APIClient

from minutes.auth.models import Token, TokenTypes

INITIAL_PASSWORD = 'initialpassword'
CHANGED_PASSWORD = 'changedpassword'


class TokenAuthenticationTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(username='testuser')
        self.user.set_password(INITIAL_PASSWORD)
        self.user.save()
        self.user_token = Token.objects.create(user=self.user, token_type=TokenTypes.AUTH)

    def test_201_for_creating_token_with_user_credentials(self):
        response = self.client.post(
            '/api/v1/token/',
            {'username': self.user.username, 'password': INITIAL_PASSWORD}
        )
        self.assertEqual(response.status_code, 201)

    def test_201_for_using_refresh_token_to_obtain_a_new_token_set(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.post(
            '/api/v1/token/',
            {'username': self.user.username, 'password': INITIAL_PASSWORD}
        )
        refresh_token = response.json()['refresh_token_key']
        response = self.client.post(
            '/api/v1/token-refresh/',
            {'refresh_token': refresh_token}
        )
        self.assertEqual(response.status_code, 201)
