from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=120, null=True, blank=True, verbose_name='Телефон')
    image = models.ImageField(upload_to='profile_img/', default='/profile_img/ava_001.png',
                              null=True, blank=True, verbose_name='Аватар')
    country = models.CharField(max_length=120, null=True, blank=True, verbose_name='Страна')

    STATUS_CHOICES = (('Менеджер', 'Менеджер'), ('Пользователь', 'Пользователь'))
    status = models.CharField(max_length=250, verbose_name='Статус', choices=STATUS_CHOICES, null=True, blank=True)

    is_blocked = models.BooleanField(default=False, verbose_name='Блокировка пользователя')

    token = models.CharField(max_length=100, verbose_name='Токен', null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ("managers", "Can view and block users"),
        ]

    def __str__(self):
        return self.email
