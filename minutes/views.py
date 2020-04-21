from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from minutes.models import MeetingSeries, SubItem, AgendaItem, Decision, Meeting, Participant
from minutes.permissions import ParticipantReadOnly, OwnerReadWrite

from minutes.serializers import UserSerializer, MeetingSeriesSerializer, MeetingSerializer, DecisionSerializer, \
    SubItemSerializer, AgendaItemSerializer, ParticipantSerializer


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
        IsAuthenticated & (ParticipantReadOnly | OwnerReadWrite)
    ]
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.owners.add(self.request.user)


class DecisionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Decision.objects.all()
    serializer_class = DecisionSerializer


class AgendaItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = AgendaItem.objects.all()
    serializer_class = AgendaItemSerializer


class SubItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SubItem.objects.all()
    serializer_class = SubItemSerializer
