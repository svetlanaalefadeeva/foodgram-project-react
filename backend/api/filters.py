from django_filters import rest_framework as filters

from cookbook.models import Recipe
from ingredients.models import Ingredient
from tags.models import Tag


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Ingredient
        fields = ['name']


class RecepeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = filters.CharFilter(
        method='filter_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    def filter_favorited(self, queryset, filter_name, filter_value):
        if filter_value:
            return queryset.filter(
                favorites__user=self.request.user
            )
        return queryset

    def get_is_in_shopping_cart(self, queryset, filter_name, filter_value):
        if filter_value:
            return queryset.filter(
                shopping_cart__user=self.request.user
            )
        return queryset

    class Meta:
        model = Recipe
        fields = [
            'tags',
            'is_favorited',
            'is_in_shopping_cart',
            'author'
        ]
