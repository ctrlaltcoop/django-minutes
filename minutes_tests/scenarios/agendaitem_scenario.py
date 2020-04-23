from django.utils import timezone

from minutes.models import AgendaMeetingItem, Meeting
from minutes_tests.scenarios.meeting_scenario import MeetingScenario


class AgendaItemScenario(MeetingScenario):
    def __init__(self):
        super().__init__()
        self.agenda_item = AgendaMeetingItem.objects.create(meeting=self.meeting)
        self.another_agenda_item = AgendaMeetingItem.objects.create(meeting=self.another_meeting)
        self.meeting_2 = Meeting.objects.create(
            name="Test Meeting 2",
            date=timezone.now(),
            series=self.test_meeting_series
        )

        self.meeting_2.add_user_as_participant(self.participant)
        self.meeting_2_agenda_item = AgendaMeetingItem.objects.create(meeting=self.meeting_2)

        self.another_meeting.add_user_as_participant(self.nobody)
