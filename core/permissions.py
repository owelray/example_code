from rest_framework import permissions

from user.constants import USER_ROLE_ADMIN, USER_ROLE_USER

__all__ = (
    'IsAdminRole',
    'IsViewerRole'
)


class IsAdminRole(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == USER_ROLE_ADMIN)


class IsViewerRole(permissions.BasePermission):

    def has_permission(self, request, view):
        # allow all POST requests
        if request.method == 'GET':
            return True
        return bool(request.user and request.user.role == USER_ROLE_USER)
