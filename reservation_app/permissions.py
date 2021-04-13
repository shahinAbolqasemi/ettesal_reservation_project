from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsScheduler(permissions.BasePermission):
    """
    This permission is for check request.user that is scheduler
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.check_group('scheduler'))


class IsSchedulerOrCustomer(permissions.BasePermission):
    """
    This permission is for check request.user that is scheduler
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.check_any_groups(['customer', 'scheduler']))


class IsAdminOrModifyOnly(permissions.BasePermission):
    """
    This permission is for check request.user that is admin.
    if not can only modify retrieve objects.
    customer can only change your self information
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_superuser or
            (request.user.check_group('scheduler') and request.method not in ['POST', 'DELETE']) or
            (request.user.check_group('customer') and request.method not in ['POST', 'DELETE'])
        )


class IsAdminOrModifierSchedulerOrReadOnly(permissions.BasePermission):
    """
    This permission is for check request.user that is admin.
    if is admin give full access
    if scheduler give update access
    if customer give view your self information
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            (
                    request.user.is_superuser or
                    (request.user.check_group('scheduler') and request.method != 'POST')
            )
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    This permission is for check request.user that is admin.
    if not can only read information
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_superuser
        )


class IsAdminOrSchedulerViewer(permissions.BasePermission):
    """
    This permission is for check request.user that is admin.
    if scheduler can only read
    """

    def has_permission(self, request, view):
        return bool(
            request.user and
            (
                    request.user.is_superuser or
                    (request.user.check_group('scheduler') and request.method == 'GET')
            )
        )
