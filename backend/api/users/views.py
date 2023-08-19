from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.pagination import CustomPagination
from users.models import (
    CustomUser,
    Subscription
)
from api.users.serializers import (
    CreateSubscriptionSerializer,
    UserSubscribeSerializer
)


class CoustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    pagination_class = CustomPagination

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        queryset = CustomUser.objects.filter(
            subscriptions__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = UserSubscribeSerializer(
            pages,
            many=True,
            context={
                'request': request
            }
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, **kwargs):
        author_id = self.kwargs.get('id')
        user = request.user
        author = get_object_or_404(
            CustomUser,
            id=author_id
        )
        serializer = CreateSubscriptionSerializer(
            data={
                'user': user.id,
                'author': author.id
            },
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(
        detail=True,
        methods=['delete'],
        permission_classes=[permissions.IsAuthenticated])
    def delete(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(
            CustomUser,
            id=author_id
        )
        subscription = get_object_or_404(
            Subscription,
            user=user,
            author=author)
        subscription.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
