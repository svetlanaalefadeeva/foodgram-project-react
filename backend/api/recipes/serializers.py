import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from api.ingredients.serializers import (
    IngredientsAddSerializer,
    IngredientSerializer
)
from api.tags.serializers import TagSerializer
from api.users.serializers import UserSerializer
from cookbook.models import (
    Favorite,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
)
from tags.models import Tag


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='ingredient.id',
        required=False
    )
    name = serializers.CharField(
        source='ingredient.name',
        read_only=True
    )
    ingredient = IngredientSerializer(
        read_only=True
    )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = [
            'id',
            'name',
            'measurement_unit',
            'amount',
            'ingredient'
        ]


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(
        read_only=True
    )
    ingredients = RecipeIngredientSerializer(
        many=True,
        source='recipe_ingredients'
    )
    image = Base64ImageField(
        required=False,
        allow_null=True
    )
    amount = RecipeIngredientSerializer(
        many=True,
        read_only=True
    )
    tags = TagSerializer(
        many=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = [
            'is_favorited',
            'is_in_shopping_cart'
        ]

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(
                user=request.user,
                recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ShoppingCart.objects.filter(
                user=request.user,
                recipe=obj).exists()
        return False


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = (
            'user',
            'recipe'
        )

    def validate(self, data):
        request = self.context['request']
        user = request.user
        recipe = data['recipe']

        if request.method == 'POST':
            if Favorite.objects.filter(
                user=user,
                recipe=recipe
            ).exists():
                raise serializers.ValidationError(
                    {'errors': 'Рецепт уже есть в избранном'},
                )
        if request.method == 'DELETE' and not Favorite.objects.filter(
            user=user,
            recipe=recipe
        ).exists():
            raise serializers.ValidationError(
                'Рецепт не найден в избранном'
            )
        return data


class AddtoShoppingCartSerializator(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = (
            'user',
            'recipe'
        )

    def validate(self, data):
        request = self.context['request']
        user = request.user
        recipe = data['recipe']

        if request.method == 'POST':
            if ShoppingCart.objects.filter(
                user=user,
                recipe=recipe
            ).exists():
                raise serializers.ValidationError(
                    {'errors': 'Рецепт уже есть в корзине'},
                )
        if request.method == 'DELETE' and not ShoppingCart.objects.filter(
            user=user,
            recipe=recipe
        ).exists():
            raise serializers.ValidationError(
                'Рецепт не найден в корзине'
            )
        return data


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = IngredientsAddSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField(
        required=False,
        allow_null=True
    )

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = [
            'author'
        ]

    def _add_ingredients(self, ingredients, recipe): 
        for ingredient in ingredients: 
            RecipeIngredient.objects.create( 
                recipe=recipe, 
                ingredient_id=ingredient.get('id'), 
                amount=ingredient.get('amount') 
            )

    def validate(self, data):
        ingredients = data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                'Требуется хотя бы один ингредиент.'
            )
        ingredient_ids = [
            ingredient['id'] for ingredient in ingredients
        ]
        if len(set(ingredient_ids)) != len(ingredient_ids):
            raise serializers.ValidationError(
                'Дублирование ингредиентов не допускается.'
            )
        for ingredient in ingredients:
            if ingredient.get('amount') <= 0:
                raise serializers.ValidationError(
                    'Количество ингредиентов должно быть больше нуля.'
                )
        return data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self._add_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        instance.ingredients.clear()
        self._add_ingredients(ingredients, instance)
        instance.tags.set(validated_data.pop('tags'))
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeSerializer(
            instance,
            context={'request': self.context.get
                     ('request')}).data
