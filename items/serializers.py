from rest_framework import serializers

from nfts.models import ItemBalance
from .models import ItemShop


class RelatedFieldAlternative(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        self.serializer = kwargs.pop("serializer", None)
        if self.serializer is not None and not issubclass(
            self.serializer, serializers.Serializer
        ):
            raise TypeError('"serializer" is not a valid serializer class')

        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False if self.serializer else True

    def to_representation(self, instance):
        if self.serializer:
            return self.serializer(instance, context=self.context).data
        return super().to_representation(instance)


class ItemShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemShop
        exclude = ["modified_at", "created_at"]

class BuyItemInputSerializer(serializers.Serializer):
    nft_id = RelatedFieldAlternative(
        queryset=ItemShop.objects.all(),
        serializer=ItemShopSerializer,
        allow_null=False,
    )
    amount = serializers.IntegerField(allow_null=False, min_value=1)