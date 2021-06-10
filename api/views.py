from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import (UserEmailSerializer, UserTokenSerializer,
                          UsersSerializer)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt import authentication
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from .permissions import AdminOrUser

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
    serializer_class = UsersSerializer
    authentication_classes = (authentication.JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated, AdminOrUser)
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    def destroy(self, request, *args, **kwargs):
        if self.kwargs.get('username') == 'me':
            error = {
                "error": [
                    "HTTP_405_METHOD_NOT_ALLOWED"
                ]
            }
            return Response(error,
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(password=get_code(), confirmation_code=get_code())

    def get_queryset(self):
        if not self.kwargs:
            return User.objects.all()
        if self.kwargs.get('username') == 'me':
            self.kwargs['username'] = self.request.user.username
        username = self.kwargs.get('username')
        return User.objects.filter(username=username)


class AuthEmailViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserEmailSerializer

    def perform_create(self, serializer):
        username = self.request.data.get('email').split('@')[0]
        serializer.save(password=get_code(), username=username, role='user',
                        confirmation_code=get_code())


class AuthTokenViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserTokenSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        code = request.data.get('confirmation_code')
        if User.objects.filter(email=email,
                               confirmation_code=code).count() < 1:
            error = {
                "error": [
                    "HTTP_403_FORBIDDEN"
                ]
            }
            return Response(error,
                            status=status.HTTP_403_FORBIDDEN)
        user = User.objects.filter(email=email, confirmation_code=code)[0]
        token = get_tokens_for_user(user)

        return Response(token,
                        status=status.HTTP_201_CREATED)
