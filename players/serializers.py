from nfts.models import ItemBalance
from nfts.serializers import ItemBalanceSerializer
from rest_framework import serializers

from .models import Player, Transaction


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


class PlayerSerializer(serializers.ModelSerializer):
    get_current_stamina = serializers.DecimalField(max_digits=15, decimal_places=5)
    get_current_tax = serializers.DecimalField(max_digits=15, decimal_places=4)
    # is_hero_slot5_active = serializers.BooleanField()
    # is_gem_slot5_active = serializers.BooleanField()
    slot5 = RelatedFieldAlternative(
        queryset=ItemBalance.objects.all(), serializer=ItemBalanceSerializer, many=True
    )

    class Meta:
        model = Player
        exclude = ["modified_at", "created_at", "user"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ["modified_at", "created_at", "player"]


class BuyGemSlotSerializer(serializers.Serializer):
    level = serializers.IntegerField(min_value=1, max_value=100)

    def validate(self, data):
        """
        Check that level is 10.
        """
        if self.level == 10:
            return data
        raise serializers.ValidationError("only level 10 is allowed.")


class BuyHeroSlotSerializer(serializers.Serializer):
    level = serializers.IntegerField(min_value=1, max_value=100)

    def validate(self, data):
        """
        Check that level is 10.
        """
        if self.level == 10:
            return data
        raise serializers.ValidationError("only level 10 is allowed.")


class ClaimRewardSerializer(serializers.Serializer):
    transaction = RelatedFieldAlternative(
        queryset=Transaction.objects.all(), serializer=TransactionSerializer, many=False
    )
    signature = serializers.CharField(max_length=255, required=True, allow_blank=False)