from rest_framework import permissions

from common.permissions import OwnerSafeAction


class IsUserOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in OwnerSafeAction:
            return bool(request.user.is_authenticated)

        return False

    def has_object_permission(self, request, view, obj):
        return obj.email == request.user.email


class IsFriendOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in OwnerSafeAction:
            return bool(request.user.is_authenticated)

        return False

    def has_object_permission(self, request, view, obj):
        return obj.user.email == request.user.email
