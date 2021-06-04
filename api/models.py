import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ForeignKey


class CustomUser(AbstractUser):
    confirmation_code = models.CharField(max_length=16)
    bio = models.CharField(max_length=254, null=True, blank=True)
    role = models.CharField(max_length=50, verbose_name='Название роли',
                            null=True)
    email = models.EmailField(verbose_name='email', unique=True)


class Genre (models.Model):
    name = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(unique=True, blank=True, default=uuid.uuid1)

    def __str__(self):
        return self.name


class Category (models.Model):
    name = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=300, unique=True)
    year = models.IntegerField(blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        blank=True,
        null=True,
        related_name='titles',
    )
    description = models.TextField(blank=True)
    rating = models.FloatField(null=True)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        symmetrical=False,
        blank=True,
        related_name='titles',
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title_id = ForeignKey(Title, on_delete=models.CASCADE)
    genre_id = ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('title_id', 'genre_id'))
