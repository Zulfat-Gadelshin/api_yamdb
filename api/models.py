from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Title(models.Model):
    pass


class Review(models.Model):
    title = models.ForeignKey(Title,
                              models.SET_NULL, blank=True, null=True,
                              related_name='reviews',
                              verbose_name='Произведение')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews")

    text = models.TextField("Текст отзыва")
    created = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    score = models.IntegerField("Оценка")

    rating = models.FloatField
    # class Meta:
    #     constraints = [UniqueConstraint(
    #         fields=['user', 'following'], name='unique_follow')]


class Comments(models.Model):
    review = models.ForeignKey(Review,
                               models.SET_NULL, blank=True, null=True,
                               related_name='comments',
                               verbose_name='Отзыв')

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")

    text = models.TextField("Текст комментария")
    created = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )
