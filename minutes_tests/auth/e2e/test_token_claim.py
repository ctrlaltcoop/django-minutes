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
        self.user_claim_token = Token.objects.create(user=self.user, token_type=TokenTypes.CLAIM)

    def test_201_for_claiming_a_token_set_only_once(self):
        response = self.client.post(
            '/api/v1/token-claim/',
            {'claim_token': self.user_claim_token.key}
        )
        self.assertEqual(response.status_code, 201)
        # second time will fail
        response = self.client.post(
            '/api/v1/token-claim/',
            {'claim_token': self.user_claim_token.key}
        )
        self.assertEqual(response.status_code, 400)

    def test_201_for_claiming_a_token_and_validate_token(self):
        response = self.client.post(
            '/api/v1/token-claim/',
            {'claim_token': self.user_claim_token.key}
        )
        self.assertEqual(response.status_code, 201)
        # second time will fail
        self.client.credentials(HTTP_AUTHORIZATION='Token {0}'.format(response.json()['auth_token_key']))
        response = self.client.get(
            '/api/v1/users/{0}/'.format(self.user.id)
        )
        self.assertEqual(response.status_code, 200)
