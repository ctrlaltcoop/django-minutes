from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from minutes.models import Meeting, MeetingSeries


class MeetingTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        self.client = APIClient()
        self.user_owner = User.objects.create(username="owner")
        self.user_participant = User.objects.create(username="participant")
        self.user_nobody = User.objects.create(username="nobody")
        self.token_owner = Token.objects.create(user=self.user_owner)
        self.token_participant = Token.objects.create(user=self.user_participant)
        self.token_nobody = Token.objects.create(user=self.user_nobody)

        self.test_meeting_series = MeetingSeries.objects.create(name="Test Series")
        self.test_meeting = Meeting.objects.create(
            name="Test Meeting",
            date=timezone.now(),
            series=self.test_meeting_series
        )
        self.test_meeting.add_user_as_participant(self.user_participant)
        self.test_meeting.owners.add(self.user_owner)

    def test_401_for_unauthenticated_user_on_list(self):
        response = self.client.get('/api/v1/meeting/')
        self.assertEqual(response.status_code, 401)

    def test_401_for_unauthenticated_user_on_retrieve(self):
        response = self.client.get('/api/v1/meeting/{0}/'.format(self.test_meeting.id))
        self.assertEqual(response.status_code, 401)

    def test_200_for_authenticated_on_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_nobody.key)
        response = self.client.get('/api/v1/meeting/')
        self.assertEqual(response.status_code, 200)

    def test_403_for_nobody_on_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_nobody.key)
        response = self.client.get('/api/v1/meeting/{0}/'.format(self.test_meeting.id))
        self.assertEqual(response.status_code, 403)

    def test_403_for_nobody_on_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_nobody.key)
        response = self.client.delete('/api/v1/meeting/{0}/'.format(self.test_meeting.id))
        self.assertEqual(response.status_code, 403)

    def test_200_for_owner_on_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_owner.key)
        response = self.client.get('/api/v1/meeting/{0}/'.format(self.test_meeting.id))
        self.assertEqual(response.status_code, 200)

    def test_200_for_participant_on_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_participant.key)
        response = self.client.get('/api/v1/meeting/{0}/'.format(self.test_meeting.id))
        self.assertEqual(response.status_code, 200)

    def test_403_for_participant_on_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_participant.key)
        response = self.client.delete('/api/v1/meeting/{0}/'.format(self.test_meeting.id))
        self.assertEqual(response.status_code, 403)

    def test_204_for_owner_on_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_owner.key)
        response = self.client.delete('/api/v1/meeting/{0}/'.format(self.test_meeting.id))
        self.assertEqual(response.status_code, 204)

    def test_400_for_participant_on_retrieve_after_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_participant.key)
        response = self.client.get('/api/v1/meeting/{0}/'.format(self.test_meeting.id))
        self.assertEqual(response.status_code, 200)
        self.test_meeting.delete()
        response = self.client.get('/api/v1/meeting/{0}/'.format(self.test_meeting.id))
        self.assertEqual(response.status_code, 404)
