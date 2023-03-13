# import os

# from rest_framework.decorators import api_view
from datetime import datetime
from time import time

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import generics, mixins, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from items.models import ItemShop
from items.serializers import ItemShopSerializer, BuyItemInputSerializer

# from .models import Color, Fruit
# from .serializers import ColorSerializer

# # Create your views here.
# DEPLOY_TIMESTAMP = os.getenv("DEPLOY_TIMESTAMP", "...")


# @api_view(["GET"])
# def index(request):
#     return Response(f"server is running. last updated at {DEPLOY_TIMESTAMP}")


# @api_view(["GET"])
# def health(request):
#     return Response("ok.")


# @api_view(["GET"])
# def get_colors(request):
#     colors = Color.objects.all()
#     serializer = ColorSerializer(colors, many=True)
#     return Response(serializer.data)


# @api_view(["POST"])
# def add_color(request):
#     # colors = Color.objects.all()
#     serializer = ColorSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)
from nfts.models import ItemBalance
from nfts.serializers import ItemBalanceSerializer
from players.models import Player


class ItemList(generics.ListAPIView):
    """
    Item List
    """

    serializer_class = ItemBalanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        if current_user.get_username() == "staff":
            return ItemBalance.objects.filter(
                address="71b07e01dde0adcbeba8b635704043ec1f665e75"
            )

        return ItemBalance.objects.filter(address=current_user.get_username())

    def get(self, request, *args, **kwargs):
        try:
            query_again = self.get_queryset()
            serializer = self.get_serializer(query_again, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"message": f"Error {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ItemShopList(generics.ListAPIView):
    """
    Get list of items in shop.
    """

    queryset = ItemShop.objects.all()
    serializer_class = ItemShopSerializer


class BuyItem(generics.CreateAPIView):
    """
    Buy item in shop
    """

    serializer_class = BuyItemInputSerializer

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        current_user = self.request.user
        #current_user = get_user_model().objects.get(pk=190)

        serializer = BuyItemInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        total_price = serializer.validated_data['amount'] * serializer.validated_data['nft_id'].price

        player = Player.objects.get(user=current_user)

        if player.gold < total_price:
            return Response(status=400, data={"error": "not enough gold"})

        gold_left = player.gold - total_price

        response = {**request.data, "balance": 0, "gold_left": gold_left, "total_deduct": total_price, "expiration_date": 0,
                    "expiration_date_extended": 0}

        with transaction.atomic():
            player.gold = gold_left
            player.save()

            if serializer.validated_data['nft_id'].rental_time > 0:
                current_rental_time = int(time())
                additional_rental_time = serializer.validated_data['nft_id'].rental_time * serializer.validated_data[
                    'amount']

                try:
                    current_balance = ItemBalance.objects.get(resource=serializer.validated_data['nft_id'].nft_id,
                                                              address=current_user)
                    if current_balance.expiration_date > current_rental_time:
                        current_rental_time = current_balance.expiration_date
                except ItemBalance.DoesNotExist:
                    current_balance = ItemBalance(created_at=datetime.now(), updated_at=datetime.now(),
                                                  is_on_chain=False, address=current_user,
                                                  resource=serializer.validated_data['nft_id'].nft_id, balance=1)

                target_expiration_date = current_rental_time + additional_rental_time
                current_balance.expiration_date = target_expiration_date
                current_balance.updated_at = datetime.now()
                current_balance.save()
                response['balance'] = 1
                response['expiration_date_extended'] = additional_rental_time
                response['expiration_date'] = target_expiration_date
            else:
                try:
                    current_balance = ItemBalance.objects.get(resource=serializer.validated_data['nft_id'].nft_id,
                                                              address=current_user)
                except ItemBalance.DoesNotExist:
                    current_balance = ItemBalance(created_at=datetime.now(), updated_at=datetime.now(),
                                                  is_on_chain=False, address=current_user,
                                                  resource=serializer.validated_data['nft_id'].nft_id, balance=0)
                target_balance = str(int(current_balance.balance) + serializer.validated_data['amount'])
                current_balance.balance = target_balance
                current_balance.updated_at = datetime.now()
                current_balance.save()
                response['balance'] = target_balance

        return Response(response)
