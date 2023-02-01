from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from minutes.auth.models import Token, TokenTypes
from rest_framework.test import APIClient


class UserTestCase(LiveServerTestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.admin = User.objects.create(username='admin', is_superuser=True)
        self.admin_token = Token.objects.create(user=self.admin, token_type=TokenTypes.AUTH)
        self.user = User.objects.create(username='user')
        self.user_token = Token.objects.create(user=self.user, token_type=TokenTypes.AUTH)

    def test_401_for_retrieving_unauthenticated(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 401)

    def test_403_for_nonadmin_creating_another_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.post('/api/v1/users/', {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 403)

    def test_403_for_nonadmin_changing_another_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.patch('/api/v1/users/{0}/'.format(self.admin.id), {
            'password': 'changed'
        })
        self.assertEqual(response.status_code, 403)

    def test_200_for_admin_user_on_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.post('/api/v1/users/', {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com'
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

    '''
    Should not be able via the general UserViewSet, need extra profile viewsets for this
    '''
    def test_200_for_nonadmin_changing_own_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.patch('/api/v1/users/{0}/'.format(self.user.id), {
            'password': 'newpass'
        })
        self.assertEqual(response.status_code, 403)
