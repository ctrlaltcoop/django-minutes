from django_filters import FilterSet
from django_filters.rest_framework import filters
from minutes.models import AgendaMeetingItem


class AgendaItemFilterSet(FilterSet):
    meeting = filters.NumberFilter(field_name='meeting_id', required=True)

    class Meta:
        model = AgendaMeetingItem
        fields = ('meeting',)
