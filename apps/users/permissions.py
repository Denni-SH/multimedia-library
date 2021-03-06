from rest_framework import permissions


class HasPermissionOrReadOnly(permissions.BasePermission):
    """
    Allow object owners only to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user


class IsVerified(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_verified
