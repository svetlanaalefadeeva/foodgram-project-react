from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.pagination import CustomPagination
from .models import CustomUser, Subscription
from .serializers import UserSerializer, UserSubscribeSerializer


class CoustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagination

    @action(methods=['get'], detail=False)
    def me(self, request):
        if self.request.user.is_authenticated:
            serializer = UserSerializer(request.user,
                                        context={'request': request})
            return Response(serializer.data)
        else:
            return Response({'detail':
                            'Учетные данные не предоставлены.'},
                            status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['get'], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        pages = self.paginate_queryset(
            CustomUser.objects.filter(subscriptions__user=self.request.user)
        )
        serializer = UserSubscribeSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post', 'delete'], url_path='subscribe',
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, **kwargs):
        user = get_object_or_404(CustomUser, id=kwargs.get('id'))
        subscribe = Subscription.objects.filter(user=request.user, author=user)
        if request.method == 'POST':
            if user == request.user:
                message = {'error': 'Вы не можете подписаться на самого себя'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            obj, created = Subscription.objects.get_or_create(
                user=request.user,
                author=user
            )
            if not created:
                message = {'error': 'Вы уже подписаны на данного пользователя'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            serializer = UserSubscribeSerializer(obj,
                                                 context={'request': request})
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        if not subscribe.exists():
            message = {'error': 'Вы еще не подписаны на данного пользователя'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
