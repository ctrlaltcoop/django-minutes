from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.utils import timezone
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

    def test_401_for_invalid_header_1(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token')
        response = self.client.post(
            '/api/v1/changepassword/',
            {'old_password': 'notcorrect', 'new_password': CHANGED_PASSWORD}
        )
        self.assertEqual(response.status_code, 401)

    def test_401_for_invalid_header_2(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token A B')
        response = self.client.post(
            '/api/v1/changepassword/',
            {'old_password': 'notcorrect', 'new_password': CHANGED_PASSWORD}
        )
        self.assertEqual(response.status_code, 401)

    def test_401_for_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token oidjfgpiojd')
        response = self.client.post(
            '/api/v1/changepassword/',
            {'old_password': 'notcorrect', 'new_password': CHANGED_PASSWORD}
        )
        self.assertEqual(response.status_code, 401)

    def test_401_for_invalid_unicode(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token F\xc3\xb8\xc3\xb6\xbbB\xc3\xa5r')
        response = self.client.post(
            '/api/v1/changepassword/',
            {'old_password': 'notcorrect', 'new_password': CHANGED_PASSWORD}
        )
        self.assertEqual(response.status_code, 401)

    def test_401_for_expired_token(self):
        expired_token = Token.objects.create(
            user=self.user,
            token_type=TokenTypes.AUTH,
            expires=timezone.now() - timezone.timedelta(seconds=1)
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token {0}'.format(expired_token.key))
        response = self.client.post(
            '/api/v1/changepassword/',
            {'old_password': 'notcorrect', 'new_password': CHANGED_PASSWORD}
        )
        self.assertEqual(response.status_code, 401)

    def test_401_for_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        self.client.credentials(HTTP_AUTHORIZATION='Token {0}'.format(self.user_token.key))
        response = self.client.post(
            '/api/v1/changepassword/',
            {'old_password': 'notcorrect', 'new_password': CHANGED_PASSWORD}
        )
        self.assertEqual(response.status_code, 401)

    def test_201_for_using_refresh_token_to_obtain_a_new_token_set(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.post(
            '/api/v1/token/',
            {'username': self.user.username, 'password': INITIAL_PASSWORD}
        )
        refresh_token = response.json()['refresh_token_key']
        self.client.credentials()
        response = self.client.post(
            '/api/v1/token-refresh/',
            {'refresh_token': refresh_token}
        )
        self.assertEqual(response.status_code, 201)

    def test_400_for_using_expired_refresh_token(self):
        expired_token = Token.objects.create(
            user=self.user,
            expires=timezone.now() - timezone.timedelta(seconds=1),
            token_type=TokenTypes.REFRESH
        )
        response = self.client.post(
            '/api/v1/token-refresh/',
            {'refresh_token': expired_token.key}
        )
        self.assertEqual(response.status_code, 400)

    def test_400_for_using_invalid_refresh_token(self):
        invalid_token = 'posfdihgpodaisfghpoh0thet4593e84'
        response = self.client.post(
            '/api/v1/token-refresh/',
            {'refresh_token': invalid_token}
        )
        self.assertEqual(response.status_code, 400)
