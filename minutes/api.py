from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.status import HTTP_200_OK

from minutes.filters import AgendaItemFilterSet, AgendaSubItemFilterSet, DecisionFilterSet, RollCallVoteFilterSet, \
    AnonymousVoteFilterSet
from minutes.models import MeetingSeries, AgendaMeetingItem, Decision, Meeting, Participant, \
    AgendaSubItem, MinutesUser, VoteChoice, RollCallVote, AnonymousVote
from minutes.permissions import ParticipantReadOnly, MeetingOwnerReadWrite, Read, Create, \
    RelatedMeetingOwned, RelatedAgendaItemOwned, RelatedMeetingSeriesOwned, IsAdminUser

from minutes.serializers import MeetingSeriesSerializer, MeetingSerializer, DecisionSerializer, \
    SubItemSerializer, AgendaItemSerializer, ParticipantSerializer, VoteChoiceSerializer, RollCallVoteSerializer, \
    AnonymousVoteSerializer, FullUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    schema = AutoSchema(tags=['minutes'])
    permission_classes = [
        IsAdminUser
    ]
    queryset = User.objects.all()
    serializer_class = FullUserSerializer

    def retrieve(self, request, *args, **kwargs):
        if kwargs['pk'] == 'me':
            return Response(self.serializer_class(instance=request.user).data, HTTP_200_OK)
        return super().retrieve(request, *args, **kwargs)


class ParticipantViewSet(viewsets.ModelViewSet):
    schema = AutoSchema(tags=['minutes'])
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class MeetingSeriesViewSet(viewsets.ModelViewSet):
    schema = AutoSchema(tags=['minutes'])
    permission_classes = [IsAuthenticated]
    serializer_class = MeetingSeriesSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return MeetingSeries.objects.all()
        user = MinutesUser.from_user(self.request.user)
        return user.my_meeting_series()


class MeetingViewSet(viewsets.ModelViewSet):
    schema = AutoSchema(tags=['minutes'])
    permission_classes = [
        IsAdminUser |
        (IsAuthenticated & (ParticipantReadOnly |
         MeetingOwnerReadWrite | (RelatedMeetingSeriesOwned & Create)))
    ]
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Meeting.objects.all()
        user = MinutesUser.from_user(self.request.user)
        return user.my_meetings()

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.owners.add(self.request.user)


class DecisionViewSet(viewsets.ModelViewSet):
    schema = AutoSchema(tags=['minutes'])
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
    schema = AutoSchema(tags=['minutes'])
    permission_classes = [
        IsAuthenticated & (ParticipantReadOnly | MeetingOwnerReadWrite | (
            Create & RelatedMeetingOwned))
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
    schema = AutoSchema(tags=['minutes'])
    permission_classes = [
        IsAuthenticated & (ParticipantReadOnly | MeetingOwnerReadWrite | (
            Create & RelatedAgendaItemOwned))
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
    schema = AutoSchema(tags=['minutes'])
    permission_classes = [
        (IsAuthenticated & Read) | IsAdminUser
    ]
    serializer_class = VoteChoiceSerializer

    def get_queryset(self):
        return VoteChoice.objects.all()


class RollCallVoteViewSet(viewsets.ModelViewSet):
    schema = AutoSchema(tags=['minutes'])
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
    schema = AutoSchema(tags=['minutes'])
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
