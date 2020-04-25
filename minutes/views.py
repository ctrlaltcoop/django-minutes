from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from minutes.filters import AgendaItemFilterSet, AgendaSubItemFilterSet, DecisionFilterSet, RollCallVoteFilterSet, \
    AnonymousVoteFilterSet
from minutes.models import MeetingSeries, AgendaMeetingItem, Decision, Meeting, Participant, \
    AgendaSubItem, MinutesUser, VoteChoice, RollCallVote, AnonymousVote
from minutes.permissions import ParticipantReadOnly, MeetingOwnerReadWrite, Read, Create, \
    RelatedMeetingOwned, RelatedAgendaItemOwned, RelatedMeetingSeriesOwned

from minutes.serializers import UserSerializer, MeetingSeriesSerializer, MeetingSerializer, DecisionSerializer, \
    SubItemSerializer, AgendaItemSerializer, ParticipantSerializer, VoteChoiceSerializer, RollCallVoteSerializer, \
    AnonymousVoteSerializer, PasswordChangeSerializer, TokenSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAdminUser
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
        IsAuthenticated & (ParticipantReadOnly | MeetingOwnerReadWrite | (RelatedMeetingSeriesOwned & Create))
    ]
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    def get_queryset(self):
        user = MinutesUser.from_user(self.request.user)
        return user.my_meetings()

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
        IsAuthenticated & (ParticipantReadOnly | MeetingOwnerReadWrite | (Create & RelatedMeetingOwned))
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
        IsAuthenticated & (ParticipantReadOnly | MeetingOwnerReadWrite | (Create & RelatedAgendaItemOwned))
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


class PasswordChangeViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def create(self, request):
        serializer: PasswordChangeSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.user.check_password(serializer.data['old_password']):
            raise PermissionDenied('Old password not correct')
        request.user.set_password(serializer.data['new_password'])
        request.user.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class TokenViewSet(GenericViewSet):
    serializer_class = AuthTokenSerializer

    def create(self, request):
        serializer: AuthTokenSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token, _ = Token.objects.get_or_create(user=User.objects.get(username=serializer.data['username']))
        token_serializer = TokenSerializer(data={'token': token.key})
        token_serializer.is_valid()
        return Response(token_serializer.data, status=status.HTTP_200_OK)
