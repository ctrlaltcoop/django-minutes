from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class VoteChoiceTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.admin = User.objects.create(username='admin', is_staff=True)
        self.admin_token = Token.objects.create(user=self.admin)

    def test_401_for_creating_unauthenticated(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 401)

    def test_200_for_admin_user_on_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.post('/api/v1/users/', {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 201)

    def test_200_for_admin_changing_username_and_verify(self):
        changed_name = 'anothername'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.patch('/api/v1/users/{0}/'.format(self.admin.id), {
            'username': changed_name
        })
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/v1/users/{0}/'.format(self.admin.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], changed_name)

    def test_200_for_admin_changing_password(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.patch('/api/v1/users/{0}/'.format(self.admin.id), {
            'password': 'newpass'
        })
        self.assertEqual(response.status_code, 200)
