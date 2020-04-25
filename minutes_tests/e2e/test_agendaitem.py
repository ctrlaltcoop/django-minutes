from django.test import LiveServerTestCase
from rest_framework.test import APIClient

from minutes_tests.scenarios.agendaitem_scenario import AgendaItemScenario


class AgendaItemTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.scenario = AgendaItemScenario()

    def test_401_for_unauthenticated_user_on_list(self):
        response = self.client.get('/api/v1/agendaitem/')
        self.assertEqual(response.status_code, 401)

    def test_401_for_unauthenticated_user_on_retrieve(self):
        response = self.client.get('/api/v1/agendaitem/{0}/'.format(self.scenario.agenda_item.id))
        self.assertEqual(response.status_code, 401)

    def test_200_for_owner_on_list_containing_my_meeting(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.owner_token.key)
        response = self.client.get('/api/v1/agendaitem/')
        agendaitem_ids = [i['id'] for i in response.json()]
        self.assertIn(self.scenario.agenda_item.id, agendaitem_ids)
        self.assertNotIn(self.scenario.another_agenda_item.id, agendaitem_ids)
        self.assertEqual(response.status_code, 200)

    def test_200_for_authenticated_nobody_on_list_but_empty(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.nobody_token.key)
        response = self.client.get('/api/v1/agendaitem/')
        agendaitem_ids = [i['id'] for i in response.json()]
        self.assertEqual([self.scenario.another_agenda_item.id], agendaitem_ids)
        self.assertEqual(response.status_code, 200)

    def test_200_for_filtering_by_meeting_and_contains_only_requested(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.participant_token.key)
        response = self.client.get('/api/v1/agendaitem/', {'meeting': self.scenario.meeting.id})
        agendaitem_ids = [i['id'] for i in response.json()]
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.scenario.agenda_item.id, agendaitem_ids)
        self.assertNotIn(self.scenario.meeting_2_agenda_item.id, agendaitem_ids)

    def test_200_for_filtering_by_meeting_2_and_contains_only_requested(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.participant_token.key)
        response = self.client.get('/api/v1/agendaitem/', {'meeting': self.scenario.meeting_2.id})
        agendaitem_ids = [i['id'] for i in response.json()]
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.scenario.agenda_item.id, agendaitem_ids)
        self.assertIn(self.scenario.meeting_2_agenda_item.id, agendaitem_ids)

    def test_200_for_listing_agenda_items_and_contains_all_agenda_items(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.participant_token.key)
        response = self.client.get('/api/v1/agendaitem/')
        agendaitem_ids = [i['id'] for i in response.json()]
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.scenario.agenda_item.id, agendaitem_ids)
        self.assertIn(self.scenario.meeting_2_agenda_item.id, agendaitem_ids)

    def test_404_for_nobody_on_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.nobody_token.key)
        response = self.client.get('/api/v1/agendaitem/{0}/'.format(self.scenario.agenda_item.id))
        self.assertEqual(response.status_code, 404)

    def test_404_for_nobody_on_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.nobody_token.key)
        response = self.client.delete('/api/v1/agendaitem/{0}/'.format(self.scenario.agenda_item.id))
        self.assertEqual(response.status_code, 404)

    def test_200_for_owner_on_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.owner_token.key)
        response = self.client.get('/api/v1/agendaitem/{0}/'.format(self.scenario.agenda_item.id))
        self.assertEqual(response.status_code, 200)

    def test_200_for_participant_on_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.participant_token.key)
        response = self.client.get('/api/v1/agendaitem/{0}/'.format(self.scenario.agenda_item.id))
        self.assertEqual(response.status_code, 200)

    def test_403_for_participant_on_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.participant_token.key)
        response = self.client.delete('/api/v1/agendaitem/{0}/'.format(self.scenario.agenda_item.id))
        self.assertEqual(response.status_code, 403)

    def test_204_for_owner_on_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.owner_token.key)
        response = self.client.delete('/api/v1/agendaitem/{0}/'.format(self.scenario.agenda_item.id))
        self.assertEqual(response.status_code, 204)

    def test_400_for_participant_on_retrieve_after_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.participant_token.key)
        response = self.client.get('/api/v1/agendaitem/{0}/'.format(self.scenario.agenda_item.id))
        self.assertEqual(response.status_code, 200)
        self.scenario.agenda_item.delete()
        response = self.client.get('/api/v1/agendaitem/{0}/'.format(self.scenario.agenda_item.id))
        self.assertEqual(response.status_code, 404)

    def test_401_for_creating_for_unauthenticated_user(self):
        response = self.client.post(
            '/api/v1/agendaitem/',
            {
                'meeting': self.scenario.meeting.id,
                'name': 'Testitem',
                'description': 'some text'
            }
        )
        self.assertEqual(response.status_code, 401)

    def test_403_for_creating_on_meeting_i_dont_own(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.nobody_token.key)
        response = self.client.post(
            '/api/v1/agendaitem/',
            {
                'meeting': self.scenario.meeting.id,
                'name': 'Testitem',
                'description': 'some text'
            }
        )
        self.assertEqual(response.status_code, 403)

    def test_200_for_creating_on_meeting_i_do_own(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.owner_token.key)
        response = self.client.post(
            '/api/v1/agendaitem/',
            {
                'meeting': self.scenario.meeting.id,
                'name': 'Testitem',
                'description': 'some text'
            }
        )
        self.assertEqual(response.status_code, 201)

    def test_verify_mentions_updated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.owner_token.key)
        response = self.client.post(
            '/api/v1/agendaitem/',
            {
                'meeting': self.scenario.meeting.id,
                'name': 'Testitem',
                'description': 'test with a mention of @{0} and @{1}'.format(
                    self.scenario.owner.username,
                    self.scenario.nobody.username
                )
            }
        )
        new_agendaitem_id = response.json()['id']
        self.assertEqual(response.status_code, 201)
        self.assertEqual([self.scenario.owner.id, self.scenario.nobody.id], response.json()['mentions'])
        response = self.client.get('/api/v1/agendaitem/', {'mentions': [self.scenario.owner.id]})
        agendaitem_ids = [i['id'] for i in response.json()]
        self.assertIn(new_agendaitem_id, agendaitem_ids)
        new_agendaitem = next((i for i in response.json() if i['id'] == new_agendaitem_id), None)
        self.assertEqual(
            [self.scenario.owner.id, self.scenario.nobody.id],
            new_agendaitem['mentions']
        )
