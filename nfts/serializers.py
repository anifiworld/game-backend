from rest_framework import serializers

from nfts.models import ItemBalance


class ItemBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemBalance
        fields = "__all__"
