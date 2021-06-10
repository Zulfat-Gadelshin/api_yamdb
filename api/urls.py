from django.urls import path, include

from .views import AuthEmailViewSet, AuthTokenViewSet, UserViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('v1/auth/email', AuthEmailViewSet, basename='email')
router.register('v1/auth/token', AuthTokenViewSet, basename='token')
router.register('v1/users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
