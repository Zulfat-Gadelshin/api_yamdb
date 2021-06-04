from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Category, Genre, Title

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


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleSerializerWrite(serializers.ModelSerializer):

    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    category = serializers.SlugRelatedField(
        many=False,
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year', 'category', 'description', 'genre',)
        model = Title


class TitleSerializerRead(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'category', 'description', 'genre',)
        model = Title
