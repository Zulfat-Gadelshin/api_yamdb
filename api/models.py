from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validtate_title_year


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'admin'
        MODERATOR = 'moderator'
        USER = 'user'

    confirmation_code = models.CharField(max_length=16, verbose_name='Код')
    bio = models.CharField(max_length=254, null=True, blank=True)
    role = models.CharField(max_length=50, verbose_name='Название роли',
                            null=True, choices=Roles.choices)
    email = models.EmailField(verbose_name='email', unique=True)

    @property
    def is_admin(self):
        return self.is_superuser or self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'


class Genre(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name='Жанр')
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=300, unique=True,
        verbose_name='Категория'
    )
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=300, unique=True, verbose_name='Название'
    )
    year = models.IntegerField(
        blank=True, verbose_name='Год выхода',
        db_index=True,
        validators=[
            validtate_title_year
        ])
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        blank=True,
        null=True,
        related_name='titles',
    )
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр',
        symmetrical=False,
        blank=True,
        related_name='titles',
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('title_id', 'genre_id'),
                name='title_genre'),
        )


class Review(models.Model):
    title = models.ForeignKey(Title,

                              on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='Произведение')
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="reviews")

    text = models.TextField("Текст отзыва")
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    score = models.IntegerField("Оценка", validators=[
        MaxValueValidator(10),
        MinValueValidator(1)
    ])


class Comment(models.Model):
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               blank=True, null=True,
                               related_name='comments',
                               verbose_name='Отзыв')
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='comments',
                              verbose_name='Произведение')

    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="comments")

    text = models.TextField("Текст комментария")
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )
