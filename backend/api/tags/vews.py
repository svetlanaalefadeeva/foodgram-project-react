from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from rest_framework.response import Response

from api.tags.serializers import TagSerializer
from tags.models import Tag


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None
