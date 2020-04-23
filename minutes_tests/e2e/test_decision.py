from django.test import LiveServerTestCase
from rest_framework.test import APIClient

from minutes_tests.scenarios.decision_scenario import DecisionScenario


class DecisionTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.scenario = DecisionScenario()

    def test_401_for_unauthenticated_user_on_list(self):
        response = self.client.get('/api/v1/decision/')
        self.assertEqual(response.status_code, 401)

    def test_401_for_unauthenticated_user_on_retrieve(self):
        response = self.client.get('/api/v1/decision/{0}/'.format(self.scenario.agenda_item.id))
        self.assertEqual(response.status_code, 401)

    def test_200_for_owner_on_list_containing_my_meeting(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.owner_token.key)
        response = self.client.get('/api/v1/decision/')
        decision_ids = [i['id'] for i in response.json()]
        self.assertIn(self.scenario.decision.id, decision_ids)
        self.assertNotIn(self.scenario.another_decision.id, decision_ids)
        self.assertEqual(response.status_code, 200)

    def test_200_for_authenticated_on_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.nobody_token.key)
        response = self.client.get('/api/v1/decision/')
        self.assertEqual(response.status_code, 200)

    def test_200_for_filtering_by_meeting_and_contains_only_requested(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.participant_token.key)
        response = self.client.get('/api/v1/decision/', {'agenda_item': self.scenario.agenda_item.id})
        decision_ids = [i['id'] for i in response.json()]
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.scenario.decision.id, decision_ids)
        self.assertNotIn(self.scenario.another_decision.id, decision_ids)

    def test_200_for_filtering_by_meeting_2_and_contains_only_requested(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.participant_token.key)
        response = self.client.get('/api/v1/decision/', {'agenda_item': self.scenario.meeting_2_agenda_item.id})
        decision_ids = [i['id'] for i in response.json()]
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.scenario.decision.id, decision_ids)
        self.assertIn(self.scenario.meeting_2_agenda_item_decision.id, decision_ids)

    def test_200_for_listing_agenda_items_and_contains_all_agenda_items(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.participant_token.key)
        response = self.client.get('/api/v1/decision/')
        decision_ids = [i['id'] for i in response.json()]
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.scenario.decision.id, decision_ids)
        self.assertIn(self.scenario.meeting_2_agenda_item_decision.id, decision_ids)

    def test_404_for_nobody_on_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.nobody_token.key)
        response = self.client.get('/api/v1/decision/{0}/'.format(self.scenario.decision.id))
        self.assertEqual(response.status_code, 404)

    def test_404_for_nobody_on_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.nobody_token.key)
        response = self.client.delete('/api/v1/decision/{0}/'.format(self.scenario.decision.id))
        self.assertEqual(response.status_code, 404)

    def test_200_for_owner_on_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.owner_token.key)
        response = self.client.get('/api/v1/decision/{0}/'.format(self.scenario.decision.id))
        self.assertEqual(response.status_code, 200)

    def test_200_for_participant_on_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.participant_token.key)
        response = self.client.get('/api/v1/decision/{0}/'.format(self.scenario.decision.id))
        self.assertEqual(response.status_code, 200)

    def test_403_for_participant_on_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.participant_token.key)
        response = self.client.delete('/api/v1/decision/{0}/'.format(self.scenario.decision.id))
        self.assertEqual(response.status_code, 403)

    def test_204_for_owner_on_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.owner_token.key)
        response = self.client.delete('/api/v1/decision/{0}/'.format(self.scenario.decision.id))
        self.assertEqual(response.status_code, 204)

    def test_400_for_participant_on_retrieve_after_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.participant_token.key)
        response = self.client.get('/api/v1/decision/{0}/'.format(self.scenario.decision.id))
        self.assertEqual(response.status_code, 200)
        self.scenario.agenda_item.delete()
        response = self.client.get('/api/v1/decision/{0}/'.format(self.scenario.decision.id))
        self.assertEqual(response.status_code, 404)
