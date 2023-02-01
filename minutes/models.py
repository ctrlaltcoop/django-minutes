import re

from django.db import models
from django.db.models import CASCADE, PROTECT, SET_NULL

from django.contrib.auth.models import User


class MinutesUser(User):
    class Meta:
        proxy = True

    @classmethod
    def from_user(cls, user: User):
        return cls.objects.get(pk=user.pk)

    def my_meetings(self):
        return self.meetings_owned.all() | \
               Meeting.objects.filter(participants__user_id=self.id)

    def my_meeting_series(self):
        return self.meetingseries_owned.all() | \
                MeetingSeries.objects.filter(participants__user_id=self.id)


class MeetingItemMixin:
    meeting: 'Meeting'

    def is_owned_by(self, user: User) -> bool:
        return user in self.meeting.owners.all()

    def is_participant(self, user: User) -> bool:
        return self.meeting.participants.filter(user=user).exists()


class AgendaSubItemMixin:
    agenda_item: 'AgendaMeetingItem'

    def is_owned_by(self, user: User) -> bool:
        return user in self.agenda_item.meeting.owners.all()

    def is_participant(self, user: User) -> bool:
        return self.agenda_item.meeting.participants.filter(user=user).exists()


class MentionMixin:
    description: str
    mention_regex = r'\s[@]([\w_-]+)'

    def update_mentions(self):
        mentioned_usernames = re.findall(self.mention_regex, self.description)
        self.mentions.set(User.objects.filter(username__in=mentioned_usernames))


class MeetingSeries(models.Model):
    name = models.CharField(max_length=70)
    description = models.TextField(default='')
    owners = models.ManyToManyField(User, related_name='meetingseries_owned')

    def is_owned_by(self, user: User) -> bool:
        return user in self.owners.all()


class Meeting(models.Model):
    series = models.ForeignKey(MeetingSeries, on_delete=CASCADE)
    name = models.CharField(max_length=70)
    date = models.DateTimeField(null=False, blank=False)
    owners = models.ManyToManyField(User, related_name='meetings_owned', blank=True)

    def add_user_as_participant(self, user):
        participant = Participant(user=user, email=user.email, meeting=self, name=user.username)
        participant.save()
        return participant

    def get_participating_users(self):
        return User.objects.filter(meeting_participations__in=self.participants.all())

    def is_owned_by(self, user: User) -> bool:
        return user in self.owners.all()

    def is_participant(self, user: User) -> bool:
        return user in self.get_participating_users()


class Participant(models.Model):
    name = models.CharField(max_length=70)
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=True, related_name='meeting_participations')
    email = models.EmailField(null=True, blank=True)
    meeting = models.ForeignKey(Meeting, related_name='participants', on_delete=CASCADE)
    attended = models.BooleanField(default=False)


class AgendaMeetingItem(models.Model, MeetingItemMixin, MentionMixin):
    meeting = models.ForeignKey(Meeting, on_delete=CASCADE)
    name = models.CharField(max_length=70)
    description = models.TextField()
    mentions = models.ManyToManyField(User)

    def save(self, **kwargs):
        super().save(**kwargs)
        self.update_mentions()


class AgendaSubItem(models.Model, AgendaSubItemMixin, MentionMixin):
    agenda_item = models.ForeignKey(AgendaMeetingItem, on_delete=CASCADE)
    name = models.CharField(max_length=70)
    description = models.TextField()
    mentions = models.ManyToManyField(User)

    def save(self, **kwargs):
        super().save(**kwargs)
        self.update_mentions()


class Decision(models.Model, AgendaSubItemMixin):
    agenda_item = models.ForeignKey(AgendaMeetingItem, on_delete=CASCADE)
    name = models.CharField(max_length=70)
    description = models.TextField()


class VoteChoice(models.Model):
    name = models.CharField(max_length=40)
    color_code = models.IntegerField(default=16711680)


class Vote(models.Model):
    vote_class = models.ForeignKey(VoteChoice, on_delete=PROTECT)
    decision = models.ForeignKey(Decision, on_delete=CASCADE)

    class Meta:
        abstract = True


class AnonymousVote(Vote):
    amount = models.IntegerField()

    def is_owned_by(self, user: User) -> bool:
        return User.objects \
            .filter(meetings_owned__agendameetingitem__decision__anonymousvote=self) \
            .filter(id=user.id) \
            .exists()

    def is_participant(self, user: User) -> bool:
        return User.objects \
            .filter(meeting_participations__meeting__agendameetingitem__decision__anonymousvote=self) \
            .filter(id=user.id) \
            .exists()


class RollCallVote(Vote):
    user = models.ForeignKey(User, on_delete=PROTECT, related_name='rollcall_votes')

    def is_owned_by(self, user: User) -> bool:
        return User.objects \
            .filter(meetings_owned__agendameetingitem__decision__rollcallvote=self) \
            .filter(id=user.id) \
            .exists()

    def is_participant(self, user: User) -> bool:
        return User.objects \
            .filter(meeting_participations__meeting__agendameetingitem__decision__rollcallvote=self) \
            .filter(id=user.id) \
            .exists()
