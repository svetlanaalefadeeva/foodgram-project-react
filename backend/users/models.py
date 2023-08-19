from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import validate_username


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True, 
        validators=[
            validate_username,
            UnicodeUsernameValidator(),
            ],
        verbose_name='Имя пользователя',
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия',
    )
    email = models.EmailField(
        unique=True,
        verbose_name = 'email'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username', 
        'password', 
        'first_name', 
        'last_name'
    ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscription(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='подписчики'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='подписки'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
                ),
            models.CheckConstraint(
                check=~models.Q(
                    author=models.F('user')
                    ),
                name='no_self_subscription',
                violation_error_message=(
                    'Подписаться на самого себя нельзя.'
                    )
                ),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user.username} - {self.author.username}'
