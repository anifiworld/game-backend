from rest_framework import serializers

from nfts.models import ItemBalance
from .models import (
    Gem,
    GemAttribute,
    GemUser,
    HeroClass,
    HeroInfo,
    HeroRank,
    HeroRarity,
    HeroType,
    HeroUser,
)


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


class HeroSerializer(serializers.ModelSerializer):
    hero_class = serializers.StringRelatedField()

    class Meta:
        model = HeroType
        exclude = ["modified_at", "created_at"]


class HeroInListSerializer(serializers.ModelSerializer):
    hero_class = serializers.StringRelatedField()

    class Meta:
        model = HeroType
        fields = ["hero_class", "name"]


class HeroRaritySerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroRarity
        fields = ["name"]


class HeroRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroRank
        fields = ["value"]


class HeroInfoSerializer(serializers.ModelSerializer):
    # nft_id = serializers.CharField()
    calculated_str = serializers.IntegerField(min_value=0)
    calculated_agi = serializers.IntegerField(min_value=0)
    calculated_vit = serializers.IntegerField(min_value=0)
    calculated_int = serializers.IntegerField(min_value=0)
    calculated_hp = serializers.IntegerField(min_value=0)
    calculated_atk = serializers.IntegerField(min_value=0)
    calculated_matk = serializers.IntegerField(min_value=0)
    calculated_def = serializers.IntegerField(min_value=0)
    calculated_aspd = serializers.IntegerField(min_value=0)
    level = serializers.IntegerField()
    current_exp = serializers.IntegerField()
    need_exp = serializers.IntegerField()
    rank = RelatedFieldAlternative(
        queryset=HeroRank.objects.all(), serializer=HeroRankSerializer
    )

    rarity = RelatedFieldAlternative(
        queryset=HeroRarity.objects.all(), serializer=HeroRaritySerializer
    )

    hero_type = RelatedFieldAlternative(
        queryset=HeroType.objects.all(), serializer=HeroInListSerializer
    )

    # hero_nft_id = serializers.CharField(max_length=255)
    # team_slot = serializers.IntegerField()
    # exp = serializers.IntegerField()
    #
    # hero = RelatedFieldAlternative(
    #     queryset=HeroType.objects.all(), serializer=HeroInListSerializer
    # )

    class Meta:
        model = HeroInfo
        exclude = ["id", "owner", "modified_at", "created_at"]


class HeroUserBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroUser
        fields = "__all__"


class HeroUserSerializer(serializers.ModelSerializer):
    info = RelatedFieldAlternative(
        queryset=HeroInfo.objects.all(), serializer=HeroInfoSerializer
    )

    class Meta:
        model = HeroUser
        exclude = ["rank", "owner", "created_at", "updated_at"]


# class HeroUserSerializer(serializers.Serializer):
#     nft_id = serializers.CharField(max_length=255)
#     calculated_str = serializers.IntegerField(min_value=0)
#     calculated_agi = serializers.IntegerField(min_value=0)
#     calculated_vit = serializers.IntegerField(min_value=0)
#     calculated_int = serializers.IntegerField(min_value=0)
#     calculated_hp = serializers.IntegerField(min_value=0)
#     calculated_atk = serializers.IntegerField(min_value=0)
#     calculated_matk = serializers.IntegerField(min_value=0)
#     calculated_def = serializers.IntegerField(min_value=0)
#     calculated_aspd = serializers.IntegerField(min_value=0)
#     rarity = RelatedFieldAlternative(
#         queryset=HeroRarity.objects.all(), serializer=HeroRaritySerializer
#     )
#     rank = RelatedFieldAlternative(
#         queryset=HeroRank.objects.all(), serializer=HeroRankSerializer
#     )
#     hero = RelatedFieldAlternative(
#         queryset=HeroType.objects.all(), serializer=HeroInListSerializer
#     )
# hero_info = RelatedFieldAlternative(
#     queryset=HeroInfo.objects.all(), serializer=HeroInfoSerializer
# )

# class Meta:
#     model = HeroOnChain
#     exclude = ["updated_at", "created_at"]


class HeroUserSlotSerializer(serializers.Serializer):
    slot1 = RelatedFieldAlternative(
        queryset=HeroUser.objects.filter(is_deleted=False),
        serializer=HeroUserSerializer,
        allow_null=True,
    )
    slot2 = RelatedFieldAlternative(
        queryset=HeroUser.objects.filter(is_deleted=False),
        serializer=HeroUserSerializer,
        allow_null=True,
    )
    slot3 = RelatedFieldAlternative(
        queryset=HeroUser.objects.filter(is_deleted=False),
        serializer=HeroUserSerializer,
        allow_null=True,
    )
    slot4 = RelatedFieldAlternative(
        queryset=HeroUser.objects.filter(is_deleted=False),
        serializer=HeroUserSerializer,
        allow_null=True,
    )
    slot5 = RelatedFieldAlternative(
        queryset=HeroUser.objects.filter(is_deleted=False),
        serializer=HeroUserSerializer,
        allow_null=True,
    )


# class HeroUserSlotListInputSerializer(serializers.ListSerializer):
#     hero_slot = HeroUserSlotInputSerializer(many=True)

#     def validate(self, hero_slots):
#         # if 1 <= len(hero_slot) <= 5:
#         #     print("validd")
#         #     return hero_slot
#         if len(hero_slots) != 5:
#             raise serializers.ValidationError("hero slots are invalid.")

#         return hero_slots

#     def update(self, validated_data):
#         tracks_data = validated_data.pop("tracks")
#         album = Album.objects.create(**validated_data)
#         for track_data in tracks_data:
#             Track.objects.create(album=album, **track_data)
#         return album


class GemAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GemAttribute
        exclude = ["modified_at", "created_at"]


class GemSerializer(serializers.ModelSerializer):
    attribute = RelatedFieldAlternative(
        queryset=Gem.objects.all(), serializer=GemAttributeSerializer
    )

    class Meta:
        model = Gem
        exclude = ["modified_at", "created_at"]


class GemUserSerializer(serializers.ModelSerializer):
    resource = serializers.SerializerMethodField()
    equpped_heroes = serializers.SerializerMethodField()

    class Meta:
        model = ItemBalance
        exclude = ["id", "address", "created_at", "is_on_chain"]

    def get_resource(self, obj):
        resource = Gem.objects.get(pk=obj.resource)
        return GemSerializer(resource).data

    def get_equpped_heroes(self, obj):
        heroes = HeroInfo.objects.filter(owner=obj.address, herouser__is_deleted=False)
        equpped_heroes = GemUser.objects.filter(gem=obj.resource, hero__in=heroes)
        return equpped_heroes.values_list('hero__nft_id', flat=True)


class GemSlotInputSerializer(serializers.Serializer):
    slot1 = RelatedFieldAlternative(
        queryset=Gem.objects.all(),
        serializer=GemSerializer,
        allow_null=True,
    )
    slot2 = RelatedFieldAlternative(
        queryset=Gem.objects.all(),
        serializer=GemSerializer,
        allow_null=True,
    )
    slot3 = RelatedFieldAlternative(
        queryset=Gem.objects.all(),
        serializer=GemSerializer,
        allow_null=True,
    )
    slot4 = RelatedFieldAlternative(
        queryset=Gem.objects.all(),
        serializer=GemSerializer,
        allow_null=True,
    )
    slot5 = RelatedFieldAlternative(
        queryset=Gem.objects.all(),
        serializer=GemSerializer,
        allow_null=True,
    )


class GemBuySerializer(serializers.Serializer):
    nft_id = serializers.CharField(max_length=255)
    amount = serializers.IntegerField(min_value=1, max_value=10)
