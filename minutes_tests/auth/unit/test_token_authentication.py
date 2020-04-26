from unittest.mock import MagicMock

from django.test import TestCase

from minutes.auth.authentication import TokenAuthentication


class TokenAuthenticationTest(TestCase):
    def setUp(self) -> None:
        self.authenticator = TokenAuthentication()

    def test_keyword_is_token(self):
        self.assertEqual(self.authenticator.authenticate_header(MagicMock()), 'Token')
