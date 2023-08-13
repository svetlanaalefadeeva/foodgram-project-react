from django_filters import rest_framework as filters
from cookbook.models import Ingredient, Recipe
from users.models import CustomUser


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ['name']


class RecepeFilter(filters.FilterSet):
    tags = filters.CharFilter(field_name='tags__slug', method='filter_tags')
    is_favorited = filters.CharFilter(method='filter_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart')
    author = filters.ModelChoiceFilter(queryset=CustomUser.objects.all())

    def filter_tags(self, queryset, slug, tags):
        tags = self.request.query_params.getlist('tags')
        return queryset.filter(tags__slug__in=tags).distinct()

    def filter_favorited(self, queryset, filter_name, filter_value):
        if filter_value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, filter_name, filter_value):
        if filter_value:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ['tags', 'is_favorited', 'is_in_shopping_cart']
