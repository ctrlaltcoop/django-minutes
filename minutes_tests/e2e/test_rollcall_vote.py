from django.test import LiveServerTestCase
from rest_framework.test import APIClient

from minutes_tests.scenarios.rollcall_vote_scenario import RollCallVoteScenario


class RollCallVoteTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.scenario = RollCallVoteScenario()

    def test_401_for_unauthenticated_user_on_list(self):
        response = self.client.get('/api/v1/rollcallvote/')
        self.assertEqual(response.status_code, 401)

    def test_401_for_unauthenticated_user_on_retrieve(self):
        response = self.client.get('/api/v1/rollcallvote/{0}/'.format(self.scenario.rollcall_vote.id))
        self.assertEqual(response.status_code, 401)

    def test_200_for_owner_on_list_containing_my_meeting(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.owner_token.key)
        response = self.client.get('/api/v1/rollcallvote/')
        vote_ids = [i['id'] for i in response.json()['results']]
        self.assertIn(self.scenario.rollcall_vote.id, vote_ids)
        self.assertNotIn(self.scenario.another_rollcall_vote.id, vote_ids)
        self.assertEqual(response.status_code, 200)

    def test_200_for_authenticated_on_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.nobody_token.key)
        response = self.client.get('/api/v1/rollcallvote/')
        self.assertEqual(response.status_code, 200)

    def test_200_for_filtering_by_meeting_and_contains_only_requested(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.participant_token.key)
        response = self.client.get('/api/v1/rollcallvote/', {'decision': self.scenario.decision.id})
        vote_ids = [i['id'] for i in response.json()['results']]
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.scenario.rollcall_vote.id, vote_ids)
        self.assertNotIn(self.scenario.another_rollcall_vote.id, vote_ids)

    def test_200_for_filtering_by_meeting_2_and_contains_only_requested(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.participant_token.key)
        response = self.client.get(
            '/api/v1/rollcallvote/',
            {'decision': self.scenario.meeting_2_agenda_item_decision.id}
        )
        vote_ids = [i['id'] for i in response.json()['results']]
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.scenario.rollcall_vote.id, vote_ids)
        self.assertIn(self.scenario.meeting_2_rollcallvote.id, vote_ids)

    def test_200_for_listing_agenda_items_and_contains_all_agenda_items(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.participant_token.key)
        response = self.client.get('/api/v1/rollcallvote/')
        vote_ids = [i['id'] for i in response.json()['results']]
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.scenario.rollcall_vote.id, vote_ids)
        self.assertIn(self.scenario.meeting_2_rollcallvote.id, vote_ids)

    def test_404_for_nobody_on_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.nobody_token.key)
        response = self.client.get('/api/v1/rollcallvote/{0}/'.format(self.scenario.rollcall_vote.id))
        self.assertEqual(response.status_code, 404)

    def test_404_for_nobody_on_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.nobody_token.key)
        response = self.client.delete('/api/v1/rollcallvote/{0}/'.format(self.scenario.rollcall_vote.id))
        self.assertEqual(response.status_code, 404)

    def test_200_for_owner_on_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.owner_token.key)
        response = self.client.get('/api/v1/rollcallvote/{0}/'.format(self.scenario.rollcall_vote.id))
        self.assertEqual(response.status_code, 200)

    def test_200_for_participant_on_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.participant_token.key)
        response = self.client.get('/api/v1/rollcallvote/{0}/'.format(self.scenario.rollcall_vote.id))
        self.assertEqual(response.status_code, 200)

    def test_403_for_participant_on_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.participant_token.key)
        response = self.client.delete('/api/v1/rollcallvote/{0}/'.format(self.scenario.rollcall_vote.id))
        self.assertEqual(response.status_code, 403)

    def test_204_for_owner_on_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.owner_token.key)
        response = self.client.delete('/api/v1/rollcallvote/{0}/'.format(self.scenario.rollcall_vote.id))
        self.assertEqual(response.status_code, 204)

    def test_400_for_participant_on_retrieve_after_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.participant_token.key)
        response = self.client.get('/api/v1/rollcallvote/{0}/'.format(self.scenario.rollcall_vote.id))
        self.assertEqual(response.status_code, 200)
        self.scenario.rollcall_vote.delete()
        response = self.client.get('/api/v1/rollcallvote/{0}/'.format(self.scenario.rollcall_vote.id))
        self.assertEqual(response.status_code, 404)
