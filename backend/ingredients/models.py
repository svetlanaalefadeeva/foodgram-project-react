from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента')
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
        )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
            fields=
            ['name',
             'measurement_unit'
             ],
            name='unique_ingredient'
            )
        ]

    def __str__(self):
        return self.name
