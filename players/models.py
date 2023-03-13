# Create your models here.
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count
from django.utils import timezone

from app.constants import rental_team_slot_20, rental_gem_slot_20, rental_gem_slot_40, rental_team_slot_40
from heroes.models import HeroInfo, GemUser, Gem, HeroUser
from nfts.models import ItemBalance

User = get_user_model()


def default_team_slot_dict():
    return {
        "slot1": None,
        "slot2": None,
        "slot3": None,
        "slot4": None,
        "slot5": None,
    }


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="player")
    # use username instead of address
    # address = models.CharField(max_length=255, default="", blank=True, null=True)
    stamina_last_updated_value = models.DecimalField(
        default=100.0, max_digits=15, decimal_places=5
    )
    stamina_last_updated = models.DateTimeField(default=timezone.now)
    coin_earned = models.DecimalField(max_digits=78, decimal_places=0, default=0)
    coin_pending = models.DecimalField(max_digits=78, decimal_places=0, default=0)
    coin_processing = models.DecimalField(max_digits=78, decimal_places=0, default=0)

    coin_last_withdrawn = models.DateTimeField(default=timezone.now)
    is_banned = models.BooleanField(default=False)
    is_newcomer = models.BooleanField(default=True)

    gold = models.IntegerField(default=0)

    team_slot = models.JSONField(default=default_team_slot_dict)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    game_play_stage = models.ForeignKey('stages.GamePlayStage', default=None, null=True, on_delete=models.RESTRICT,
                                        related_name='player_game_play_stage')

    def __str__(self) -> str:
        return self.user.get_username()

    def remove_all_equip_gem(self):
        heroes = HeroInfo.objects.filter(owner=self.user.get_username())
        GemUser.objects.filter(hero__in=heroes).delete()

    def get_max_gem_rental_slot_level(self):
        max_level = 0
        if self.slot5.filter(resource=rental_gem_slot_40).count() > 0:
            max_level = 40
        elif self.slot5.filter(resource=rental_gem_slot_20).count() > 0:
            max_level = 20
        return max_level

    def get_max_hero_rental_slot_level(self):
        max_level = 0
        if self.slot5.filter(resource=rental_team_slot_40).count() > 0:
            max_level = 40
        elif self.slot5.filter(resource=rental_team_slot_20).count() > 0:
            max_level = 20
        return max_level

    def remove_unusable_gem(self):
        max_level = self.get_max_gem_rental_slot_level()
        heroes = HeroInfo.objects.filter(owner=self.user.get_username(), herouser__is_deleted=False)
        GemUser.objects.filter(slot=5, hero__in=heroes, gem__in=Gem.objects.filter(level_needed__gt=max_level)).delete()

    def remove_unusable_heroes(self):
        max_level = self.get_max_hero_rental_slot_level()
        timestamp = int(timezone.now().timestamp()) - (24 * 60 * 60)
        for x in [1, 2, 3, 4, 5]:
            if self.team_slot['slot' + str(x)] is not None and self.team_slot['slot' + str(x)] != '':
                try:
                    hero = HeroInfo.objects.get(nft_id=self.team_slot['slot' + str(x)], owner=self.user.get_username(),
                                                herouser__is_deleted=False, herouser__timestamp__lte=timestamp)
                    if x == 5 and hero.level > max_level:
                        self.team_slot['slot' + str(x)] = None
                        self.save()
                except HeroInfo.DoesNotExist:
                    self.team_slot['slot' + str(x)] = None
                    self.save()

    def is_gem_balance_consistent(self):
        gem_balance = ItemBalance.objects.filter(address=self.user.get_username(), resource__in=Gem.objects.all())
        heroes = HeroInfo.objects.filter(owner=self.user.get_username(), herouser__is_deleted=False)
        current_use_balances = GemUser.objects.filter(hero__in=heroes, gem__isnull=False).values('gem').annotate(
            count=Count('gem'))
        require_balance = {x['gem']: int(x['count']) for x in current_use_balances}
        for gem_id in require_balance:
            count = require_balance[gem_id]
            try:
                if int(gem_balance.get(resource=gem_id).balance) < count:
                    return False
            except ItemBalance.DoesNotExist:
                self.remove_all_equip_gem()
                return False
        return True

    def sync_gem_equip(self):
        self.remove_unusable_gem()
        if not self.is_gem_balance_consistent():
            self.remove_all_equip_gem()

    def sync_hero_slot(self):
        self.remove_unusable_heroes()

    def validate_gem_equip(self):
        # TODO Validate gem
        return True

    def validate_hero_slot(self):
        # TODO Validate hero
        return True

    @property
    def team_slot_data(self):
        timestamp = int(timezone.now().timestamp()) - (24 * 60 * 60)
        owned_hero = HeroUser.objects.filter(owner=self.user.get_username(), is_deleted=False,
                                             transferred_at__lte=timestamp)
        res = {}
        for x in [1, 2, 3, 4, 5]:
            if self.team_slot["slot" + str(x)] is not None:
                try:
                    res["slot" + str(x)] = owned_hero.get(pk=self.team_slot["slot" + str(x)])
                except HeroUser.DoesNotExist:
                    res["slot" + str(x)] = None
            else:
                res["slot" + str(x)] = None

        return res

    @property
    def slot5(self):
        date_string = timezone.now().timestamp()
        rental_list = [
            rental_team_slot_20,
            rental_team_slot_40,
            rental_gem_slot_20,
            rental_gem_slot_40,
        ]
        return (
            ItemBalance.objects.filter(address=self.user.get_username())
            .filter(expiration_date__gt=int(date_string))
            .filter(balance__gte=1)
            .filter(resource__in=rental_list)
        )

    @property
    def get_current_stamina(self) -> Decimal:
        previous_stamina = self.stamina_last_updated_value
        max_stamina = 100
        multiplier = max_stamina / (1 * 60 * 60 * 24)  # max in a day

        # if full then return
        if previous_stamina >= max_stamina:
            self.stamina_last_updated = timezone.now()
            self.save()
            return previous_stamina

        time_diff_since_stamina_last_updated = (
                timezone.now() - self.stamina_last_updated
        )
        addition_stamina = (
                time_diff_since_stamina_last_updated.total_seconds() * multiplier
        )
        # print("pre")
        # print(previous_stamina)
        # print("add")
        # print(addition_stamina)
        current_stamina = previous_stamina + Decimal(addition_stamina)

        if current_stamina > max_stamina:
            current_stamina = Decimal(max_stamina)

            self.stamina_last_updated_value = current_stamina
            self.stamina_last_updated = timezone.now()
            self.save()
            return current_stamina

        self.stamina_last_updated_value = current_stamina
        self.stamina_last_updated = timezone.now()
        self.save()
        return current_stamina

    @property
    def get_current_tax(self) -> Decimal:
        time_diff_since_last_withdraw = (
                timezone.now() - self.coin_last_withdrawn
        )
        current_tax = (1 - (time_diff_since_last_withdraw.total_seconds() / (15 * 24 * 60 * 60))) * 0.3
        if current_tax < 0:
            current_tax = Decimal(0)
        # print("pre")
        # print(previous_stamina)
        # print("add")
        # print(addition_stamina)
        return current_tax


class Transaction(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 1, "PENDING"
        COMPLETED = 2, "COMPLETED"
        FAILED = 3, "FAILED"

    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="player_transaction")
    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.PENDING
    )
    tx_hash = models.CharField(max_length=100, null=True, blank=True)
    nounce = models.CharField(primary_key=True, max_length=32, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    tx_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    claim_amount = models.DecimalField(max_digits=78, decimal_places=0, default=0)
    # uuid.uuid4().hex
