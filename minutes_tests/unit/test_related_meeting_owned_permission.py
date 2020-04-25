from unittest import mock
from unittest.mock import PropertyMock, MagicMock, ANY

from django.http import HttpRequest
from django.test import TestCase
from rest_framework.request import Request

from minutes.permissions import RelatedMeetingOwned


class RelatedMeetingOwnedTest(TestCase):

    def setUp(self) -> None:
        self.permission = RelatedMeetingOwned()

    @mock.patch('rest_framework.request.Request.data', new_callable=PropertyMock)
    def test_related_meeting_owned_permission_while_no_meeting_in_request(self, request_data_mock):
        request_data_mock.return_value = {}
        self.assertFalse(self.permission.has_permission(Request(HttpRequest()), None))

    @mock.patch('minutes.models.MinutesUser.from_user', new_callable=MagicMock)
    @mock.patch('minutes.models.MinutesUser.meetings_owned', new_callable=MagicMock)
    @mock.patch('rest_framework.request.Request.data', new_callable=PropertyMock)
    def test_related_meeting_owned_permission_while_meeting_in_request_but_meeting_not_owned(
            self,
            request_data_mock,
            meetings_owned_mock,
            from_user_mock,
    ):
        request_data_mock.return_value = {
            'meeting': 1
        }

        meetings_owned_mock.filter.return_value.exists = MagicMock(return_value=False)
        from_user_mock.return_value.meetings_owned = meetings_owned_mock

        self.assertFalse(self.permission.has_permission(Request(HttpRequest()), None))

    @mock.patch('minutes.models.MinutesUser.from_user', new_callable=MagicMock)
    @mock.patch('minutes.models.MinutesUser.meetings_owned', new_callable=MagicMock)
    @mock.patch('rest_framework.request.Request.data', new_callable=PropertyMock)
    def test_related_meeting_owned_permission_while_meeting_in_request_and_meeting_owned(
            self,
            request_data_mock,
            meetings_owned_mock,
            from_user_mock,
    ):
        request_data_mock.return_value = {
            'meeting': 1
        }

        meetings_owned_mock.filter.return_value.exists = MagicMock(return_value=True)
        from_user_mock.return_value.meetings_owned = meetings_owned_mock

        self.assertTrue(self.permission.has_permission(Request(HttpRequest()), None))
