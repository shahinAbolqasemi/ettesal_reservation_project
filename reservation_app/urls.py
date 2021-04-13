from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SessionRequestViewSet, ParticipantViewSet, ParticipantAssignmentViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'session-requests', SessionRequestViewSet, basename='session_request')
router.register(r'participants', ParticipantViewSet, basename='participants')
router.register(r'participant-assignments', ParticipantAssignmentViewSet, basename='participant_assignments')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
