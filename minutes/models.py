from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE, PROTECT, SET_NULL


class MeetingItemMixin:
    meeting: 'Meeting'

    def is_owned_by(self, user: User) -> bool:
        return user in self.meeting.owners

    def is_moderated_by(self, user: User) -> bool:
        return user in self.meeting.moderators

    def is_participant(self, user: User) -> bool:
        return user in self.meeting.participants


class AgendaSubItemMixin:
    agenda_item: 'AgendaMeetingItem'

    def is_owned_by(self, user: User) -> bool:
        return user in self.agenda_item.meeting.owners

    def is_moderated_by(self, user: User) -> bool:
        return user in self.agenda_item.meeting.moderators

    def is_participant(self, user: User) -> bool:
        return user in self.agenda_item.meeting.participants


class MeetingSeries(models.Model):
    name = models.CharField(max_length=70)
    description = models.TextField(default='')
    owners = models.ManyToManyField(User, related_name='meetingseries_owned')
    moderators = models.ManyToManyField(User, related_name='meetingseries_moderated')

    def is_owned_by(self, user: User) -> bool:
        return user in self.owners.all()

    def is_moderated_by(self, user: User) -> bool:
        return user in self.moderators.all()


class Meeting(models.Model):
    series = models.ForeignKey(MeetingSeries, on_delete=CASCADE)
    name = models.CharField(max_length=70)
    date = models.DateTimeField(null=False, blank=False)
    owners = models.ManyToManyField(User, related_name='meetings_owned', blank=True)
    moderators = models.ManyToManyField(User, related_name='meetings_moderated', blank=True)

    def add_user_as_participant(self, user):
        participant = Participant(user=user, email=user.email, meeting=self, name=user.username)
        participant.save()
        return participant

    def get_participating_users(self):
        return User.objects.filter(meeting_participations__in=self.participants.all())

    def is_owned_by(self, user: User) -> bool:
        return user in self.owners.all()

    def is_moderated_by(self, user: User) -> bool:
        return user in self.moderators.all()

    def is_participant(self, user: User) -> bool:
        return user in self.get_participating_users()


class Participant(models.Model):
    name = models.CharField(max_length=70)
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=True, related_name='meeting_participations')
    email = models.EmailField(null=True, blank=True)
    meeting = models.ForeignKey(Meeting, related_name='participants', on_delete=CASCADE)
    attended = models.BooleanField(default=False)


class AgendaMeetingItem(models.Model, MeetingItemMixin):
    meeting = models.ForeignKey(Meeting, on_delete=CASCADE)
    name = models.CharField(max_length=70)
    description = models.TextField()


class AgendaSubItem(models.Model, AgendaSubItemMixin):
    agenda_item = models.ForeignKey(AgendaMeetingItem, on_delete=CASCADE)
    name = models.CharField(max_length=70)
    description = models.TextField()
    order_with_respect_to = Meeting


class Decision(models.Model, AgendaSubItemMixin):
    agenda_item = models.ForeignKey(AgendaMeetingItem, on_delete=CASCADE)
    name = models.CharField(max_length=70)
    description = models.TextField()


class VoteChoice(models.Model):
    name = models.CharField(max_length=40)
    color_code = models.IntegerField()


class Vote(models.Model):
    amount = models.IntegerField()
    vote_class = models.ForeignKey(VoteChoice, on_delete=PROTECT, related_name='used_by')
    decision = models.ForeignKey(Decision, on_delete=CASCADE, related_name='votes')

    def is_owned_by(self, user: User) -> bool:
        return user in self.decision.agenda_item.meeting.owners

    def is_moderated_by(self, user: User) -> bool:
        return user in self.decision.agenda_item.meeting.moderators

    def is_participant(self, user: User) -> bool:
        return user in self.decision.agenda_item.meeting.participants
