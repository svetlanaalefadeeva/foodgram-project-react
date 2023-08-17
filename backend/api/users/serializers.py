from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from cookbook.models import Recipe
from users.models import (
    CustomUser,
    Subscription
)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'is_subscribed'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(
            validated_data['password']
        )
        user.save()
        return user

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(
                'Нельзя создать пользователя с именем "me"!'
            )
        return value

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user=self.context.get('request').user,
            author=obj).exists() if self.context.get(
            'request') and self.context.get(
            'request').user.is_authenticated else False


class SubscriptionRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
        read_only_fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class UserSubscribeSerializer(UserSerializer):
# остаивла этот вариант наследования, так поля не переопределяю
    recipes_count = serializers.SerializerMethodField(read_only=True)  
    recipes = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + [
            'recipes_count',
            'recipes',
        ]
        read_only_fields = [
            'email',
            'username',
            'first_name',
            'last_name',
        ]

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = SubscriptionRecipeSerializer(
            recipes,
            many=True,
            read_only=True
        )
        return serializer.data

    def get_is_subscribed(self, obj):
        return True


class CreateSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = (
            'user',
            'author',
        )

    def validate(self, attrs):
        user = self.context['request'].user
        author = attrs['author']
        if Subscription.objects.filter(
            user=user,
            author=author
        ).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора'
            )
        if user == author:
            raise serializers.ValidationError(
                'Вы не можете подписаться на самого себя'
            )
        return attrs
