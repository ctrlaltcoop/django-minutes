from django.test import LiveServerTestCase
from rest_framework.test import APIClient

from minutes_tests.scenarios.vote_choice_scenario import VoteChoiceScenario


class VoteChoiceTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.scenario = VoteChoiceScenario()

    def test_401_for_unauthenticated_user_on_list(self):
        response = self.client.get('/api/v1/votechoice/')
        self.assertEqual(response.status_code, 401)

    def test_200_for_authenticated_user_on_list_with_all_items(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.user_token.key)
        response = self.client.get('/api/v1/votechoice/')
        votechoice_ids = [i['id'] for i in response.json()]
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.scenario.vote_choice_1.id, votechoice_ids)
        self.assertIn(self.scenario.vote_choice_2.id, votechoice_ids)
        self.assertIn(self.scenario.vote_choice_3.id, votechoice_ids)

    def test_403_for_authenticated_user_on_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.user_token.key)
        response = self.client.post('/api/v1/votechoice/', {'name': 'please, create me'})
        self.assertEqual(response.status_code, 403)

    def test_403_for_authenticated_user_on_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.user_token.key)
        response = self.client.delete('/api/v1/votechoice/{0}/'.format(self.scenario.vote_choice_1.id))
        self.assertEqual(response.status_code, 403)

    def test_403_for_authenticated_user_on_patch(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.user_token.key)
        response = self.client.patch('/api/v1/votechoice/{0}/'.format(self.scenario.vote_choice_1.id), {'name': 'change'})
        self.assertEqual(response.status_code, 403)

    def test_200_for_admin_user_on_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.admin_token.key)
        votechoice_name = 'please, create me'
        response = self.client.post('/api/v1/votechoice/', {'name': votechoice_name})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], votechoice_name)

    def test_200_for_admin_user_on_patch(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.admin_token.key)
        votechoice_name = 'please, change me'
        response = self.client.patch(
            '/api/v1/votechoice/{0}/'.format(self.scenario.vote_choice_1.id),
            {'name': votechoice_name}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], votechoice_name)

    def test_204_for_admin_user_on_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.scenario.admin_token.key)
        response = self.client.delete('/api/v1/votechoice/{0}/'.format(self.scenario.vote_choice_1.id))
        self.assertEqual(response.status_code, 204)
        response = self.client.get('/api/v1/votechoice/{0}/'.format(self.scenario.vote_choice_1.id))
        self.assertEqual(response.status_code, 404)
