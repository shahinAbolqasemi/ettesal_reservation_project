from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from reservation_app.serializers import UserAdminSerializer, UserPublicSerializer
from . import permissions
from rest_framework import permissions as base_permissions


class UserViewSet(ModelViewSet):
    """
    This ViewSet is view for List , Retrieve, Update and Delete (all) user
    but with permissions
    """
    serializer_class = UserPublicSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [
        base_permissions.IsAuthenticated,
        permissions.IsScheduler,
        permissions.IsAdminOrReadOnly
    ]

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return UserAdminSerializer
        return super().get_serializer_class()

