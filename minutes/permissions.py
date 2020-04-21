from rest_framework.permissions import BasePermission, SAFE_METHODS

CREATE_METHODS = ['POST']
MODIFY_METHODS = ['PATCH', 'PUT']
DELETE_METHODS = ['DELETE']


class UserInOwners(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in getattr(obj, 'owners').all()


class UserInSeriesOwners(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.series.owners.all()


class IsParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id in obj.participants.values_list('user', flat=True)


class Create(BasePermission):
    def has_permission(self, request, view):
        return request.method in CREATE_METHODS


class ReadObject(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class ModifyObject(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in MODIFY_METHODS


class DeleteObject(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in DELETE_METHODS


MeetingOwner = (UserInSeriesOwners | UserInOwners)

OwnerReadWrite = (MeetingOwner & ModifyObject) | (MeetingOwner & DeleteObject) | (MeetingOwner & ReadObject)
ParticipantReadOnly = (IsParticipant & ReadObject)
