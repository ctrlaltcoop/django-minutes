from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.permissions import IsAdminUser as IsAdminUserBase

from minutes.models import MinutesUser, AgendaMeetingItem, MeetingSeries

CREATE_METHODS = ['POST']
MODIFY_METHODS = ['PATCH', 'PUT']
DELETE_METHODS = ['DELETE']


class IsOwnedByUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_owned_by(request.user)


class IsSeriesOwnedByUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        series = getattr(obj, 'series', None)
        if series:
            return obj.series.is_owned_by(request.user)
        return False


class IsParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_participant(request.user)


class Create(BasePermission):
    def has_permission(self, request, view):
        return request.method in CREATE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in CREATE_METHODS


class Read(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class Modify(BasePermission):
    def has_permission(self, request, view):
        return request.method in MODIFY_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in MODIFY_METHODS


class Delete(BasePermission):
    def has_permission(self, request, view):
        return request.method in DELETE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in DELETE_METHODS


class RelatedMeetingSeriesOwned(BasePermission):
    def has_permission(self, request, view):
        series_id = request.data.get('series', None)
        if not series_id:
            return False
        try:
            series = MeetingSeries.objects.get(pk=series_id)
            return request.user in series.owners.all()
        except MeetingSeries.DoesNotExist:
            return False


class RelatedMeetingOwned(BasePermission):
    def has_permission(self, request, view):
        meeting_id = request.data.get('meeting', None)
        if not meeting_id:
            return False

        user = MinutesUser.from_user(request.user)
        return user.meetings_owned.filter(pk=meeting_id).exists()


class RelatedAgendaItemOwned(BasePermission):
    def has_permission(self, request, view):
        agendaitem_id = request.data.get('agenda_item', None)
        if not agendaitem_id:
            return False
        user = MinutesUser.from_user(request.user)
        return AgendaMeetingItem.objects.filter(meeting__in=user.meetings_owned.all()).filter(pk=agendaitem_id).exists()


class OwnUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsAdminUser(BasePermission):
    """
    A custom IsAdminUser class which also checks being admin user on object permissions
    With the base class returning always True for has_object_permission it'll cause trouble
    if you want to use it with & on other object permissions.
    """
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


MeetingOwner = (IsSeriesOwnedByUser | IsOwnedByUser)

MeetingOwnerReadWrite = (MeetingOwner & Modify) |\
                        (MeetingOwner & Delete) |\
                        (MeetingOwner & Read)

ParticipantReadOnly = (IsParticipant & Read)

ReadOwnUser = OwnUser & Read
