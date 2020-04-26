from django.contrib.auth.models import User
from django.core import mail
from django.test import LiveServerTestCase
from rest_framework.test import APIClient

from minutes.auth.models import Token, TokenTypes


class InvitationTestCase(LiveServerTestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.inviting_user = User.objects.create(username='inviter')
        self.inviting_user_token = Token.objects.create(user=self.inviting_user, token_type=TokenTypes.AUTH)
        self.friends_email_address = 'friend@sketchyprovider.com'

    def test_invite_user_sends_email(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.inviting_user_token.key)
        response = self.client.post('/api/v1/invitation/', {
            'username': 'my_friend',
            'email': self.friends_email_address
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.friends_email_address, mail.outbox[0].to)

    def test_invite_user_with_email_already_registered(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.inviting_user_token.key)
        User.objects.create(username='dude', email=self.friends_email_address)
        response = self.client.post('/api/v1/invitation/', {
            'username': 'my_friend',
            'email': self.friends_email_address
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(mail.outbox), 0)
