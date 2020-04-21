from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from minutes.models import Meeting, MeetingSeries, Decision, AgendaItem, SubItem, Participant


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MeetingSeriesSerializer(ModelSerializer):
    class Meta:
        model = MeetingSeries
        fields = '__all__'


class MeetingSerializer(ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['id', 'name', 'owners', 'moderators', 'participants']


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
        model = AgendaItem
        fields = '__all__'


class SubItemSerializer(ModelSerializer):
    class Meta:
        model = SubItem
        fields = '__all__'
