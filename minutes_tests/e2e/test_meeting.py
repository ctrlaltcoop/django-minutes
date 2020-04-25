from django.test import LiveServerTestCase
from django.utils import timezone
from rest_framework.test import APIClient

from minutes_tests.scenarios.meeting_scenario import MeetingScenario


class MeetingTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.scenario = MeetingScenario()

    def test_401_for_unauthenticated_user_on_list(self):
        response = self.client.get('/api/v1/meeting/')
        self.assertEqual(response.status_code, 401)

    def test_401_for_unauthenticated_user_on_retrieve(self):
        response = self.client.get('/api/v1/meeting/{0}/'.format(self.scenario.meeting.id))
        self.assertEqual(response.status_code, 401)

    def test_401_for_unauthenticated_user_on_create(self):
        response = self.client.post('/api/v1/meeting/', {
            'name': 'Test meeting',
            'series': self.scenario.test_meeting_series.id
        })
        self.assertEqual(response.status_code, 401)

    def test_403_for_creating_a_meeting_on_a_series_i_dont_own(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.series_owner_token.key)
        response = self.client.post('/api/v1/meeting/', {
            'name': 'Test meeting',
            'series': self.scenario.another_test_meeting_series.id,
            'date': timezone.now()
        })
        self.assertEqual(response.status_code, 403)

    def test_200_for_authenticated_on_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.series_owner_token.key)
        response = self.client.post('/api/v1/meeting/', {
            'name': 'Test meeting',
            'series': self.scenario.test_meeting_series.id,
            'date': timezone.now()
        })
        self.assertEqual(response.status_code, 201)

    def test_200_for_owner_on_list_containing_my_meeting(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.owner_token.key)
        response = self.client.get('/api/v1/meeting/')
        meeting_ids = [i['id'] for i in response.json()]
        self.assertIn(self.scenario.meeting.id, meeting_ids)
        self.assertNotIn(self.scenario.another_meeting.id, meeting_ids)
        self.assertEqual(response.status_code, 200)

    def test_200_for_authenticated_on_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.nobody_token.key)
        response = self.client.get('/api/v1/meeting/')
        self.assertEqual(response.status_code, 200)

    def test_403_for_nobody_on_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.nobody_token.key)
        response = self.client.get('/api/v1/meeting/{0}/'.format(self.scenario.meeting.id))
        self.assertEqual(response.status_code, 404)

    def test_403_for_nobody_on_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.nobody_token.key)
        response = self.client.delete('/api/v1/meeting/{0}/'.format(self.scenario.meeting.id))
        self.assertEqual(response.status_code, 404)

    def test_200_for_owner_on_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.owner_token.key)
        response = self.client.get('/api/v1/meeting/{0}/'.format(self.scenario.meeting.id))
        self.assertEqual(response.status_code, 200)

    def test_200_for_participant_on_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.participant_token.key)
        response = self.client.get('/api/v1/meeting/{0}/'.format(self.scenario.meeting.id))
        self.assertEqual(response.status_code, 200)

    def test_403_for_participant_on_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.participant_token.key)
        response = self.client.delete('/api/v1/meeting/{0}/'.format(self.scenario.meeting.id))
        self.assertEqual(response.status_code, 403)

    def test_204_for_owner_on_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.owner_token.key)
        response = self.client.delete('/api/v1/meeting/{0}/'.format(self.scenario.meeting.id))
        self.assertEqual(response.status_code, 204)

    def test_400_for_participant_on_retrieve_after_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.participant_token.key)
        response = self.client.get('/api/v1/meeting/{0}/'.format(self.scenario.meeting.id))
        self.assertEqual(response.status_code, 200)
        self.scenario.meeting.delete()
        response = self.client.get('/api/v1/meeting/{0}/'.format(self.scenario.meeting.id))
        self.assertEqual(response.status_code, 404)
