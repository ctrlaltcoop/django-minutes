from unittest.case import TestCase

from minutes.apps import MinutesConfig


class AppTest(TestCase):
    def test_app_name(self):
        self.assertEqual(MinutesConfig.name, 'minutes')
