from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from ingredients.models import Ingredient
from tags.models import Tag

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Изображение',
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient, 
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(
                1,
                message='Минимальное значение 1!'
            )
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'author',
                    'name'
                ],
                name='unique_recipe'
            )
        ]

    def __str__(self):
        return self.name

    @property
    def ingredients_list(self):
        return self.ingredients.values_list(
            'name',
            flat=True
        )

    @property
    def ingredients_measurement_unit_list(self):
        return self.ingredients.values_list(
            'measurement_unit',
            flat=True
        )

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='recipe_ingredients'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                1,
                message='Минимальное количество 1!'
                )
        ]
    )

    class Meta:
        ordering = ['ingredient']
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество ингридиентов'
        constraints = [
            models.UniqueConstraint(
            fields=[
                'recipe',
                'ingredient'
                ],
            name='unique_recepe_s_ingredient'
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт'
    )
    amount = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'recipe'
                ],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт')

    class Meta:
        unique_together = (
            'user',
            'recipe'
            )
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return f'{self.user.username} - {self.recipe}'
