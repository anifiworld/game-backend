import os

from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Color, Fruit
from .serializers import ColorSerializer, StringSerializer

# Create your views here.
DEPLOY_TIMESTAMP = os.getenv("DEPLOY_TIMESTAMP", "...")


class index(generics.GenericAPIView):
    # queryset = None
    serializer_class = StringSerializer
    # lookup_field = None

    def get(self, request):
        text = {"value": "Hello, world! (deployed at {})".format(DEPLOY_TIMESTAMP)}
        # serializer = StringSerializer(string)
        # return Response(serializer.data)
        return Response(text)


class health(generics.GenericAPIView):
    # queryset = None
    serializer_class = StringSerializer
    # lookup_field = None

    def get(self, request):
        text = {"value": "ok."}
        # serializer = StringSerializer(string)
        # return Response(serializer.data)
        return Response(text)


# @api_view(["GET"])
# def health(request):
#     string = {"value": "ok."}
#     serializer = StringSerializer(string)
#     return Response(serializer.data)


@api_view(["GET"])
def get_colors(request):
    colors = Color.objects.all()
    serializer = ColorSerializer(colors, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def add_color(request):
    # colors = Color.objects.all()
    serializer = ColorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
