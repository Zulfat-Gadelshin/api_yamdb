from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AuthEmailViewSet, AuthTokenViewSet, UserViewSet
from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register('auth/email', AuthEmailViewSet, basename='email')
router.register('auth/token', AuthTokenViewSet, basename='token')
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('v1/', include(router.urls)),
]
