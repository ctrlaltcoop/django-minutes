from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from minutes.filters import AgendaItemFilterSet, AgendaSubItemFilterSet, DecisionFilterSet, RollCallVoteFilterSet, \
    AnonymousVoteFilterSet
from minutes.models import MeetingSeries, AgendaMeetingItem, Decision, Meeting, Participant, \
    AgendaSubItem, MinutesUser, VoteChoice, RollCallVote, AnonymousVote
from minutes.permissions import ParticipantReadOnly, MeetingOwnerReadWrite, Read

from minutes.serializers import UserSerializer, MeetingSeriesSerializer, MeetingSerializer, DecisionSerializer, \
    SubItemSerializer, AgendaItemSerializer, ParticipantSerializer, VoteChoiceSerializer, RollCallVoteSerializer, \
    AnonymousVoteSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,

    ]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ParticipantViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class MeetingSeriesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = MeetingSeries.objects.all()
    serializer_class = MeetingSeriesSerializer


class MeetingViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated & (ParticipantReadOnly | MeetingOwnerReadWrite)
    ]
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    def get_queryset(self):
        my_meetings = self.request.user.meetings_owned.all() | \
                      self.request.user.meetings_moderated.all() | \
                      Meeting.objects.filter(participants__user=self.request.user)
        return my_meetings

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.owners.add(self.request.user)


class DecisionViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated & (ParticipantReadOnly | MeetingOwnerReadWrite)
    ]
    serializer_class = DecisionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DecisionFilterSet

    def get_queryset(self):
        user = MinutesUser.from_user(self.request.user)
        return Decision.objects.filter(
            agenda_item__meeting__in=user.my_meetings()
        )


class AgendaItemViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated & (ParticipantReadOnly | MeetingOwnerReadWrite)
    ]

    serializer_class = AgendaItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AgendaItemFilterSet

    def get_queryset(self):
        user = MinutesUser.from_user(self.request.user)
        return AgendaMeetingItem.objects.filter(
            meeting__in=user.my_meetings()
        )


class AgendaSubItemViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated & (ParticipantReadOnly | MeetingOwnerReadWrite)
    ]
    serializer_class = SubItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AgendaSubItemFilterSet

    def get_queryset(self):
        user = MinutesUser.from_user(self.request.user)
        return AgendaSubItem.objects.filter(
            agenda_item__meeting__in=user.my_meetings()
        )


class VoteChoiceViewSet(viewsets.ModelViewSet):
    permission_classes = [
        (IsAuthenticated & Read) | IsAdminUser
    ]
    serializer_class = VoteChoiceSerializer

    def get_queryset(self):
        return VoteChoice.objects.all()


class RollCallVoteViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated & (ParticipantReadOnly | MeetingOwnerReadWrite)
    ]
    serializer_class = RollCallVoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RollCallVoteFilterSet

    def get_queryset(self):
        user = MinutesUser.from_user(self.request.user)
        return RollCallVote.objects.filter(
            decision__agenda_item__meeting__in=user.my_meetings()
        )


class AnonymousVoteViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated & (ParticipantReadOnly | MeetingOwnerReadWrite)
    ]
    serializer_class = AnonymousVoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnonymousVoteFilterSet

    def get_queryset(self):
        user = MinutesUser.from_user(self.request.user)
        return AnonymousVote.objects.filter(
            decision__agenda_item__meeting__in=user.my_meetings()
        )
