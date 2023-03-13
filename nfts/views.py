from django.contrib.auth import get_user_model
from django.db.models import Prefetch

from app.constants import items_meta_dict
from heroes.models import HeroInfo, HeroUser
from rest_framework import generics, status
from rest_framework.response import Response

from heroes.views import sync_info
from metaMaskAuth.serializers import WalletAuthSerializer


# Create your views here.
# class NFTsView(generics.ListAPIView):
#     serializer_class = NftsSerializer

#     def get_queryset(self):
#         return Nfts.objects.filter(user=self.request.user)


class NFTMetaData(generics.ListAPIView):
    """
    NFT MetaData
    """

    def get(self, request, nft_id, *args, **kwargs):

        if nft_id.startswith("0x"):
            striped_nft_id = nft_id[2:].lower().zfill(64)
        else:
            striped_nft_id = hex(int(nft_id))[2:].zfill(64)

        decimal_id = str(int(striped_nft_id, 16))
        if decimal_id in items_meta_dict:
            return Response(items_meta_dict[decimal_id])

        hero_on_chains = HeroUser.objects.filter(pk=striped_nft_id, is_deleted=False,
                                                 is_on_chain=True).prefetch_related(
            Prefetch(
                "info",
                queryset=HeroInfo.objects.prefetch_related(
                    "rarity", "hero_type", "rank"
                ),
            ),
            "owner",
            "rank",
        ).all()

        if not hero_on_chains.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        hero_on_chain = hero_on_chains.first()

        if not get_user_model().objects.filter(username=hero_on_chain.owner_id).exists():
            serializer = WalletAuthSerializer(data={
                "public_address": '0x' + hero_on_chain.owner_id,
                "user": {
                    "username": hero_on_chain.owner_id,
                }
            })
            if serializer.is_valid():
                serializer.save()

        sync_info(hero_on_chains)

        hero_on_chain = HeroUser.objects.filter(pk=striped_nft_id, is_deleted=False, is_on_chain=True).prefetch_related(
            Prefetch(
                "info",
                queryset=HeroInfo.objects.prefetch_related(
                    "rarity", "hero_type", "rank"
                ),
            ),
            "owner",
            "rank",
        ).first()

        name = hero_on_chain.info.hero_type.name
        level = hero_on_chain.info.level
        rarity = hero_on_chain.info.rarity
        rank = hero_on_chain.info.rank

        calculated_agi = hero_on_chain.info.calculated_agi
        calculated_int = hero_on_chain.info.calculated_int
        calculated_str = hero_on_chain.info.calculated_str
        calculated_vit = hero_on_chain.info.calculated_vit

        return Response(
            {
                "description": name.capitalize()
                               + " #"
                               + str(int(striped_nft_id[-16:], 16)),
                "image": "https://api.anifi.io/heroes/user/hero_card/"
                         + striped_nft_id,
                "name": name.capitalize() + " #" + str(int(striped_nft_id[-16:], 16)) + " (" + rarity.name.capitalize() + ")",
                "owner": '0x' + hero_on_chain.owner_id,
                "id": str(int(striped_nft_id, 16)),
                "attributes": [
                    {"trait_type": "Type", "value": "Hero"},
                    {"trait_type": "Level", "display_type": "number", "value": level},
                    {"trait_type": "Rarity", "value": rarity.name.capitalize()},
                    {
                        "trait_type": "Rank",
                        "display_type": "number",
                        "value": rank.value,
                    },
                    {
                        "trait_type": "STR",
                        "display_type": "number",
                        "value": calculated_str,
                    },
                    {
                        "trait_type": "INT",
                        "display_type": "number",
                        "value": calculated_int,
                    },
                    {
                        "trait_type": "VIT",
                        "display_type": "number",
                        "value": calculated_vit,
                    },
                    {
                        "trait_type": "AGI",
                        "display_type": "number",
                        "value": calculated_agi,
                    },
                ],
            }
        )
