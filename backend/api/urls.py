from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.users.views import CoustomUserViewSet

from api.ingredients.views import IngredientViewSet
from api.recipes.views import RecipeViewSet
from api.tags.vews import TagViewSet


app_name = 'api'

router = DefaultRouter()

router.register(r'tags', TagViewSet, basename='tag')
router.register(r'users', CoustomUserViewSet, basename='user')
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'ingredients', IngredientViewSet, basename='ingredient')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
