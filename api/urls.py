from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('genres', views.GenreViewSet)
router.register('titles', views.TitleViewSet)
router.register('auth/email', views.AuthEmailViewSet, basename='email')
router.register('auth/token', views.AuthTokenViewSet, basename='token')
router.register('users', views.UserViewSet, basename='user')
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews',
    views.ReviewViewSet, 'Reviews')
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    views.CommentViewSet, 'Comments')

urlpatterns = [
    path('v1/', include(router.urls)),
]
