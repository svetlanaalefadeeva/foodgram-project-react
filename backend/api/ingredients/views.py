from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ingredients.models import Ingredient
from api.filters import IngredientFilter
from api.ingredients.serializers import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    pagination_class = None
