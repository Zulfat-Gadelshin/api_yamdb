from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers
from .filters import TitleFilter
from .models import Category, Genre, Title, Review, Comment
from .permissions import IsAdmin, IsAdminOrReadOnly, IsOwnerOrReadOnly
from .viewsets import CustomViewset

User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def get_code():
    chars = ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQ'
             'RSTUVWXYZ0123456789!@#$%^&*()-_=+')
    return get_random_string(16, chars)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UsersSerializer
    authentication_classes = (authentication.JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    queryset = User.objects.all()

    @action(detail=False, methods=('GET', 'PATCH'),
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        cur_user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(cur_user)
        if request.method == 'PATCH':
            serializer = self.get_serializer(cur_user, data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(data=request.data, role=cur_user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthEmailViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserEmailSerializer
    authentication_classes = []
    permission_classes = []

    def perform_create(self, serializer):
        serializer.get_or_create(password=get_code(), role=User.Roles.USER,
                                 confirmation_code=get_code())


class AuthTokenViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserTokenSerializer
    authentication_classes = []
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        email = serializer.data.get('email')
        code = serializer.data.get('confirmation_code')
        if not User.objects.filter(email=email,
                                   confirmation_code=code).exists():
            error = {
                "error": [
                    "HTTP_400_BAD_REQUEST"
                ]
            }
            return Response(error,
                            status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email, confirmation_code=code).first()
        token = get_tokens_for_user(user)

        return Response(token,
                        status=status.HTTP_201_CREATED)


class CategoryViewSet(CustomViewset):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ['name', ]


class GenreViewSet(CustomViewset):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (
        IsAdminOrReadOnly,
    )
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name', 'slug', ]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (
        IsAdminOrReadOnly,
    )
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    filter_class = TitleFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.TitleSerializerRead
        return serializers.TitleSerializerWrite


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        if serializer.is_valid():
            serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    )
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title, id=self.kwargs.get('title_id')
        )
        review = get_object_or_404(
            Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, title=title, review=review)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        queryset = Comment.objects.filter(title=title, review=review)

        return queryset
