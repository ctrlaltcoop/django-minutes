from unittest import mock
from unittest.mock import PropertyMock, MagicMock, ANY

from django.http import HttpRequest
from django.test import TestCase
from rest_framework.request import Request

from minutes.models import MeetingSeries
from minutes.permissions import RelatedMeetingSeriesOwned


class RelatedSeriesOwnedTest(TestCase):

    def setUp(self) -> None:
        self.permission = RelatedMeetingSeriesOwned()

    @mock.patch('rest_framework.request.Request.data', new_callable=PropertyMock)
    def test_related_series_owned_permission_while_no_meeting_in_request(self, request_data_mock):
        request_data_mock.return_value = {}
        self.assertFalse(self.permission.has_permission(Request(HttpRequest()), None))

    @mock.patch('minutes.models.MeetingSeries.objects', new_callable=MagicMock)
    @mock.patch('rest_framework.request.Request.data', new_callable=PropertyMock)
    def test_related_series_owned_permission_while_meeting_in_request_but_series_doesnt_exist(
            self,
            request_data_mock,
            meeting_series_manager,
    ):
        request_data_mock.return_value = {
            'series': 1
        }

        meeting_series_manager.get.side_effect = MeetingSeries.DoesNotExist()
        self.assertFalse(self.permission.has_permission(Request(HttpRequest()), None))
        meeting_series_manager.get.assert_called_once()

    @mock.patch('minutes.models.MeetingSeries.objects', new_callable=MagicMock)
    @mock.patch('rest_framework.request.Request.data', new_callable=PropertyMock)
    def test_related_series_owned_permission_while_meeting_in_request_and_series_owned(
            self,
            request_data_mock,
            meeting_series_manager,
    ):
        request_data_mock.return_value = {
            'series': 1
        }

        mock_user = MagicMock(name='Mock user')
        mock_request = Request(HttpRequest())
        mock_request.user = mock_user

        mock_series = MagicMock(name='Mock series')
        meeting_series_manager.get.return_value = mock_series
        mock_series.owners.all.return_value = [mock_user]

        self.assertTrue(self.permission.has_permission(mock_request, None))
        meeting_series_manager.get.assert_called_once()
        mock_series.owners.all.assert_called_once()

    @mock.patch('minutes.models.MeetingSeries.objects', new_callable=MagicMock)
    @mock.patch('rest_framework.request.Request.data', new_callable=PropertyMock)
    def test_related_series_owned_permission_while_meeting_in_request_and_series_not_owned(
            self,
            request_data_mock,
            meeting_series_manager,
    ):
        request_data_mock.return_value = {
            'series': 1
        }

        mock_user = MagicMock(name='Mock user')
        mock_request = Request(HttpRequest())
        mock_request.user = mock_user

        mock_series = MagicMock(name='Mock series')
        meeting_series_manager.get.return_value = mock_series
        mock_series.owners.all.return_value = []

        self.assertFalse(self.permission.has_permission(mock_request, None))
        meeting_series_manager.get.assert_called_once()
        mock_series.owners.all.assert_called_once()
