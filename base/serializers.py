from rest_framework import serializers

from .models import Color, Fruit


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"


class StringSerializer(serializers.Serializer):
    value = serializers.CharField()
