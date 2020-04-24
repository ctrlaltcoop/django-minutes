from django_filters import FilterSet
from django_filters.rest_framework import filters
from minutes.models import AgendaMeetingItem, AgendaSubItem, Decision, RollCallVote, AnonymousVote


class AgendaItemFilterSet(FilterSet):
    meeting = filters.NumberFilter(field_name='meeting_id', required=False)

    class Meta:
        model = AgendaMeetingItem
        fields = ('meeting',)


class AgendaSubItemFilterSet(FilterSet):
    agenda_item = filters.NumberFilter(field_name='agenda_item_id', required=False)

    class Meta:
        model = AgendaSubItem
        fields = ('agenda_item',)


class DecisionFilterSet(FilterSet):
    agenda_item = filters.NumberFilter(field_name='agenda_item_id', required=False)

    class Meta:
        model = Decision
        fields = ('agenda_item',)


class RollCallVoteFilterSet(FilterSet):
    decision = filters.NumberFilter(field_name='decision_id', required=False)

    class Meta:
        model = RollCallVote
        fields = ('decision',)


class AnonymousVoteFilterSet(FilterSet):
    decision = filters.NumberFilter(field_name='decision_id', required=False)

    class Meta:
        model = AnonymousVote
        fields = ('decision',)
