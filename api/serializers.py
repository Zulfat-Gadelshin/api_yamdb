from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Category, Comment, Genre, Review, Title

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
        fields = ('id', 'name', 'year', 'category', 'description', 'genre', 'rating',)
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    class Meta:
        fields = ('id', 'title', 'pub_date', 'text', 'score', 'author',)
        model = Review
        '''validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title']
            )
        ]'''

        '''def validate(self, data):
            title = data.get('title')
            author = data.get('author')
            review = Review.objects.filter(title=title, author=author)
            # recheck validate in this
            if review:
                raise serializers.ValidationError('not valid')
            return data'''


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    review = serializers.SlugRelatedField(
        slug_field='id',
        read_only=True,
    )

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'review', 'title')
        model = Comment
