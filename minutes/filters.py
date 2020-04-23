from django_filters import FilterSet
from django_filters.rest_framework import filters
from minutes.models import AgendaMeetingItem, AgendaSubItem, Decision


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
