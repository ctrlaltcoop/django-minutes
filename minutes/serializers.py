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
    moderators = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    owners = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = MeetingSeries
        fields = ['id', 'name', 'description', 'owners', 'moderators']


class MeetingSerializer(ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    moderators = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    owners = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    series = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Meeting
        fields = ['id', 'series', 'name', 'date', 'owners', 'moderators', 'participants']


class ParticipantSerializer(ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'


class DecisionSerializer(ModelSerializer):
    class Meta:
        model = Decision
        fields = '__all__'


class AgendaItemSerializer(ModelSerializer):
    class Meta:
        model = AgendaMeetingItem
        fields = '__all__'


class SubItemSerializer(ModelSerializer):
    class Meta:
        model = AgendaSubItem
        fields = '__all__'


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
