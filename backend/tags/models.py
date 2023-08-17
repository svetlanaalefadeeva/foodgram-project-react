from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега',
        unique=True,
    )
    color = models.CharField(
        'Цветовой HEX-код',
        unique=True,
        max_length=7,
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Цвет должен быть в формате HEX'
            )
        ]
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Slug'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
