from django.contrib import admin

from .models import (
    Favorite,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = (
        'name',
        'author',
        'image',
        'text',
        'cooking_time',
        'pub_date',
        'get_favorite'
    )
    fields = (
        ('name', 'cooking_time',),
        ('author', 'tags',),
        ('text',), ('image',)
    )
    filter_horizontal = ('tags',)
    search_fields = (
        'name',
        'author',
        'tag'
    )
    list_filter = (
        'name',
        'author__username',
        'tags__name'
    )
    empty_value_display = '-пусто-'

    def get_favorite(self, obj):
        get_favorite = Favorite.objects.filter(
            recipe=obj
        ).count()
        return get_favorite

    get_favorite.short_description = 'В избранном'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )
    search_fields = (
        'user__username',
        'recipe__name')
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )
    search_fields = (
        'user__username',
        'recipe__name'
    )
    exclude = ('amount',)
    empty_value_display = '-пусто-'
