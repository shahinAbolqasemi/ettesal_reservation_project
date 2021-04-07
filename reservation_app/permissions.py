from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from django.contrib.auth.models import Group


class UserRoles:

    @staticmethod
    def is_scheduler(user):
        try:
            user.groups.get(name='scheduler')
        except Group.DoesNotExist:
            return False
        return True


class IsScheduler(permissions.BasePermission, UserRoles):
    """
    This permission is for check request.user that is scheduler
    """

    def has_permission(self, request, view):
        return bool(request.user and self.is_scheduler(request.user))


class IsAdminOrReadOnly(permissions.BasePermission, UserRoles):
    """
    This permission is for check request.user that is scheduler
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_superuser
        )
