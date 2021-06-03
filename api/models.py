from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    confirmation_code = models.CharField(max_length=16)
    bio = models.CharField(max_length=254, null=True, blank=True)
    role = models.CharField(max_length=50, verbose_name='Название роли',
                            null=True)
    email = models.EmailField(verbose_name='email', unique=True)

