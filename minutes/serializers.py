from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from minutes.models import Meeting, MeetingSeries, Decision, AgendaMeetingItem, Participant, AgendaSubItem, \
    VoteChoice, AnonymousVote, RollCallVote


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MeetingSeriesSerializer(ModelSerializer):
    owners = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = MeetingSeries
        fields = ['id', 'name', 'description', 'owners']


class MeetingSerializer(ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    owners = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    series = serializers.PrimaryKeyRelatedField(queryset=MeetingSeries.objects.all())

    class Meta:
        model = Meeting
        fields = ['id', 'series', 'name', 'date', 'owners', 'participants']


class ParticipantSerializer(ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'


class DecisionSerializer(ModelSerializer):
    class Meta:
        model = Decision
        fields = '__all__'


class AgendaItemSerializer(ModelSerializer):
    meeting = serializers.PrimaryKeyRelatedField(queryset=Meeting.objects.all())
    mentions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = AgendaMeetingItem
        fields = ['id', 'meeting', 'name', 'description', 'mentions']


class SubItemSerializer(ModelSerializer):
    agenda_item = serializers.PrimaryKeyRelatedField(queryset=AgendaMeetingItem.objects.all())
    mentions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = AgendaSubItem
        fields = ['id', 'agenda_item', 'name', 'description', 'mentions']


class VoteChoiceSerializer(ModelSerializer):
    class Meta:
        model = VoteChoice
        fields = '__all__'


class RollCallVoteSerializer(ModelSerializer):
    class Meta:
        model = RollCallVote
        fields = '__all__'


class AnonymousVoteSerializer(ModelSerializer):
    class Meta:
        model = AnonymousVote
        fields = '__all__'


class PasswordChangeSerializer(Serializer):  # pylint: disable=W0223
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class TokenSerializer(Serializer):  # pylint: disable=W0223
    token = serializers.CharField()
