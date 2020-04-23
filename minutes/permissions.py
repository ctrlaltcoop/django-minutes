from rest_framework.permissions import BasePermission, SAFE_METHODS

CREATE_METHODS = ['POST']
MODIFY_METHODS = ['PATCH', 'PUT']
DELETE_METHODS = ['DELETE']


class IsModeratedByUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_owned_by(request.user)


class IsOwnedByUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_owned_by(request.user)


class IsSeriesOwnedByUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        series = getattr(obj, 'series', None)
        if series:
            return obj.series.is_owned_by(request.user)
        return False


class IsSeriesModeratedByUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.series.is_owned_by(request.user)


class IsParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_participant(request.user)


class Create(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

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


MeetingOwner = (IsSeriesOwnedByUser | IsOwnedByUser)

MeetingOwnerReadWrite = (MeetingOwner & Modify) | (MeetingOwner & Delete) | (MeetingOwner & Read)
ParticipantReadOnly = (IsParticipant & Read)
