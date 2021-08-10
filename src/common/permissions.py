from rest_framework import permissions

OwnerSafeAction = ['retrieve', 'metadata', 'partial_update', 'update']


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user
                    and request.user.is_authenticated
                    and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return bool(request.user
                    and request.user.is_authenticated
                    and request.user.is_staff)
