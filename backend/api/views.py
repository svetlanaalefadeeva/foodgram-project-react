from django.http import HttpResponse
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from cookbook.models import Ingredient, Favorite, Recipe, ShoppingCart, Tag

from .filters import IngredientFilter, RecepeFilter
from .pagination import CustomPagination
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeSerializer, TagSerializer)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['^name']
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecepeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return RecipeCreateSerializer
        return RecipeSerializer

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response({'errors': 'Рецепт уже есть в избранном'},
                                status=status.HTTP_400_BAD_REQUEST)
            favorite = Favorite.objects.create(user=user, recipe=recipe)
            serializer = RecipeSerializer(favorite.recipe)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            try:
                favorite = Favorite.objects.get(user=user, recipe=recipe)
                favorite.delete()
            except Favorite.DoesNotExist:
                return Response({'errors': 'Рецепт не найден в избраном'},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            return Response({'errors': 'Рецепт уже есть в в корзине'},
                            status=status.HTTP_400_BAD_REQUEST)
        cart_item = ShoppingCart.objects.create(user=user, recipe=recipe)
        serializer = RecipeSerializer(cart_item.recipe)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'],
            permission_classes=[IsAuthenticated])
    def delete(self, request, *args, **kwargs):
        recipe = self.get_object()
        user = request.user
        try:
            cart_item = ShoppingCart.objects.get(
                user=user, recipe=recipe)
            cart_item.delete()
        except ShoppingCart.DoesNotExist:
            return Response({'errors': 'Рецепт не найден в корзине'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'],
            detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        queryset = Recipe.objects.filter(shopping_cart__user=request.user)
        ingredients_dict = {}
        for recipe in queryset:
            for recipe_ingredient in recipe.recipe_ingredients.all():
                ingredient_name = recipe_ingredient.ingredient.name
                if ingredient_name in ingredients_dict:
                    ingredients_dict[ingredient_name]['amount'] += (
                        recipe_ingredient.amount)
                else:
                    ingredients_dict[ingredient_name] = {
                        'measurement_unit':
                        recipe_ingredient.ingredient.measurement_unit,
                        'amount': recipe_ingredient.amount
                    }
        file_name = 'shopping_cart.txt'
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        for ingredient, data in ingredients_dict.items():
            response.write(
                f"{ingredient} - {data['amount']} {data['measurement_unit']}\n"
            )
        return response
