import webcolors
from rest_framework import serializers
from tags.models import Tag


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        color = Hex2NameColor()
        fields = [
            'id',
            'name',
            'color',
            'slug'
            ]
        read_only_fields = [
            'id',
            'name',
            'color',
            'slug'
            ]
