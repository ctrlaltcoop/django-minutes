from django.test import LiveServerTestCase


class FrontendViewTestCase(LiveServerTestCase):
    def test_test_case_returns_an_html_page(self):
        response = self.client.get('/app/')
        self.assertEqual(response.status_code, 200)
        self.assertIsNot(response.get('Content-Type'), None)
        self.assertEqual(response.get('Content-Type'), 'text/html; charset=utf-8')
