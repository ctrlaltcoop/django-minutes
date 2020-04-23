from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.authtoken.models import Token

from minutes.models import Meeting, MeetingSeries

owner = User.objects.create(username="owner")
moderator = User.objects.create(username="moderator")
participant = User.objects.create(username="participant")
nobody = User.objects.create(username="nobody")

Token.objects.create(user=owner)
Token.objects.create(user=participant)
Token.objects.create(user=nobody)
Token.objects.create(user=moderator)


test_meeting_series = MeetingSeries.objects.create(name="Test Series")
test_meeting = Meeting.objects.create(
    name="Test Meeting",
    date=timezone.now(),
    series=test_meeting_series
)

test_meeting.add_user_as_participant(participant)
test_meeting.owners.add(owner)
test_meeting.moderators.add(moderator)
