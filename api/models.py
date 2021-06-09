from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator


class CustomUser(AbstractUser):
    confirmation_code = models.CharField(max_length=16)
    bio = models.CharField(max_length=254, null=True, blank=True)
    role = models.CharField(max_length=50, verbose_name='Название роли',
                            null=True)
    email = models.EmailField(verbose_name='email', unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
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
