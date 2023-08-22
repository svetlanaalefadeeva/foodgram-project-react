from django.db.models import Sum
from django.http import FileResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response

from cookbook.models import (
    Favorite,
    Recipe,
    ShoppingCart,
)
from api.filters import RecepeFilter
from api.pagination import CustomPagination
from api.recipes.serializers import (
    AddtoShoppingCartSerializator,
    RecipeCreateSerializer,
    RecipeSerializer,
    FavoriteSerializer,
)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination
    filterset_class = RecepeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in (
            'create',
            'update',
            'partial_update'
        ):
            return RecipeCreateSerializer
        return RecipeSerializer

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        serializer = FavoriteSerializer(
            data={
                'recipe': recipe.id,
                'user': user.id
            },
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        favorite, created = Favorite.objects.get_or_create(
            user=user,
            recipe=recipe
        )
        serializer = RecipeSerializer(favorite.recipe)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        serializer = FavoriteSerializer(
            data={
                'recipe': recipe.id,
                'user': user.id
            },
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        favorite = Favorite.objects.get(
            user=user,
            recipe=recipe
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        serializer = AddtoShoppingCartSerializator(
            data={
                'recipe': recipe.id,
                'user': user.id
            },
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        cart_item = ShoppingCart.objects.create(
            user=user,
            recipe=recipe
        )
        serializer = RecipeSerializer(
            cart_item.recipe
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(
        detail=True,
        methods=['delete'],
        permission_classes=[IsAuthenticated]
    )
    def delete(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        serializer = AddtoShoppingCartSerializator(
            data={
                'recipe': recipe.id,
                'user': user.id
            },
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        cart_item = ShoppingCart.objects.get(
            user=user,
            recipe=recipe
        )
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        queryset = Recipe.objects.filter(
            shopping_cart__user=request.user
        )
        ingredients = _create_ingredients_dict(
            queryset
        )
        content = _generate_ingredients_content(
            ingredients
        )
        response = FileResponse(
            content,
            content_type="text/plain"
        )
        response["Content-Disposition"] = (
            'attachment;filename="ingredients.txt"'
        )
        return response

def _create_ingredients_dict(queryset):
    ingredients = (
        queryset.values_list(
            'recipe_ingredients__ingredient__name',
            'recipe_ingredients__ingredient__measurement_unit'
        )
        .annotate(amount=Sum('recipe_ingredients__amount'))
    )
    return ingredients

def _generate_ingredients_content(ingredients):
    content = ''
    for ingredient in ingredients:
        ingredient, amount, measurement_unit = ingredient
        content += (
            f'{ingredient} - {measurement_unit} {amount}\n'
        )
    return content
