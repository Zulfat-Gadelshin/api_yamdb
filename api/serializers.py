from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email',)
        model = User


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email', 'confirmation_code')
        model = User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('first_name', 'last_name',
                  'username', 'bio', 'email', 'role')
        model = User
