import uuid

from django.db import IntegrityError, transaction
from django.utils import timezone

from base.web3 import transfer_reward, recover_address, check_blockchain_reward
from heroes.models import HeroInfo, HeroUser
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Player, Transaction
from .serializers import BuyGemSlotSerializer, BuyHeroSlotSerializer, PlayerSerializer, ClaimRewardSerializer, \
    TransactionSerializer


# Create your views here.


class PlayerDetail(generics.RetrieveAPIView):
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Player.objects.get(user=self.request.user)

    def get(self, request, *args, **kwargs):
        serializer = PlayerSerializer(self.get_queryset())
        return Response(serializer.data)


class GetFreeHeroes(generics.GenericAPIView):
    serializer_class = None
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Player.objects.get(user=self.request.user)

    def put(self, request, *args, **kwargs):
        player = self.get_queryset()
        if not player.is_newcomer:
            return Response({"detail": "You are not a new comer."}, status=400)
        username = self.request.user.get_username()
        current_datetime = timezone.now()
        # heroes_info = [
        #     HeroInfo(nft_id=username + "1", rarity_id=1, hero_id=1, rank_id=1, owner=self.request.user),
        #     HeroInfo(nft_id=username + "2", rarity_id=1, hero_id=2, rank_id=1, owner=self.request.user),
        #     HeroInfo(nft_id=username + "3", rarity_id=1, hero_id=3, rank_id=1, owner=self.request.user),
        # ]
        heroes_info = [
            HeroInfo(
                nft_id=f"{username}{'0' * 5}{str(i)}",
                rarity_id=1,
                hero_type_id=i,
                rank_id=0,
                owner=self.request.user,
            )
            for i in range(1, 4)
        ]
        heroes_user = [
            HeroUser(
                info_id=f"{username}{'0' * 5}{str(i)}",
                base_str=5,
                base_int=5,
                base_vit=5,
                base_agi=5,
                rank_id=0,
                owner=self.request.user,
                is_on_chain=False,
                is_deleted=False,
                created_at=current_datetime,
                updated_at=current_datetime,
                transferred_at=0
            )
            for i in range(1, 4)
        ]
        player.is_newcomer = False

        try:
            with transaction.atomic():
                for hero_info in heroes_info:
                    hero_info.save()
                for hero_user in heroes_user:
                    hero_user.save()
                player.save()
        except IntegrityError as e:
            return Response({"message": f"{str(e)}"}, status=400)
        except Exception as e:
            return Response({"message": f"{str(e)}"}, status=400)
        return Response({"message": "Successfully get free heroes."}, status=200)


class GetClaim(generics.GenericAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def get(self, request, id):
        serializer = PlayerSerializer(Player.objects.get(user__username=id))
        return Response(serializer.data)
        # return Response({"Wallet": id}, status=200)


class BuyGemSlot(generics.GenericAPIView):
    queryset = Player.objects.all()
    serializer_class = BuyGemSlotSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BuyGemSlotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # blabla
        return Response("WIP")


class BuyHeroSlot(generics.GenericAPIView):
    queryset = Player.objects.all()
    serializer_class = BuyHeroSlotSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BuyHeroSlotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # blabla
        return Response("WIP")


class ClaimReward(generics.GenericAPIView):
    serializer_class = ClaimRewardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Player.objects.get(user=self.request.user)

    def post(self, request):
        serializer = ClaimRewardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        player = self.get_queryset()
        my_transaction = serializer.validated_data['transaction']
        if my_transaction.player != player:
            return Response({"detail": "You are not the owner of this transaction."}, status=400)

        if my_transaction.status != Transaction.Status.PENDING:
            return Response({"detail": "This transaction is not pending."}, status=400)

        try:
            address = recover_address("Claim reward transaction id " + my_transaction.nounce, serializer.validated_data['signature'])
            if address.lower() != ('0x' + str(player.user)).lower():
                return Response({"detail": "Invalid signature."}, status=400)
        except Exception as e:
            return Response({"detail": f"{str(e)}"}, status=400)

        try:
            reward_target = player.coin_earned + player.coin_pending
            if check_blockchain_reward(address, reward_target) <= 0:
                return Response({"detail": "You don't have enough reward."}, status=400)
            with transaction.atomic():
                txn_hash = transfer_reward(address, reward_target)
                if txn_hash:
                    my_transaction.status = Transaction.Status.COMPLETED
                    my_transaction.tx_hash = txn_hash
                    my_transaction.tx_at = timezone.now()
                    my_transaction.save()
                    player.coin_earned = reward_target
                    player.coin_pending = 0
                    player.save()
                    return Response({"detail": "Successfully claim reward."}, status=200)
                else:
                    raise Exception("Failed to claim reward.")
        except Exception as e:
            my_transaction.status = Transaction.Status.FAILED
            my_transaction.error_message = str(e)
            my_transaction.tx_at = timezone.now()
            my_transaction.save()
            if e.args[0] == "Failed to claim reward.":
                return Response({"detail": "Failed to claim reward."}, status=400)
            else:
                return Response({"detail": f"{str(e)}"}, status=400)

    def get(self, request):
        player = self.get_queryset()
        if player.coin_pending <= 0:
            return Response({"message": "You don't have any pending reward."}, status=400)
        nounce = uuid.uuid4().hex
        message = 'Claim reward transaction id ' + nounce
        tx = Transaction.objects.create(nounce=nounce, player=player, status=Transaction.Status.PENDING, claim_amount=player.coin_pending)
        tx.save()
        return Response({"message": message, "transaction": tx.nounce, "amount": str(tx.claim_amount)})
