from ctypes import c_uint8 as uint8
from ctypes import c_uint16 as uint16

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CASCADE, Prefetch
from django.utils import timezone
from django.utils.functional import cached_property

User = get_user_model()


class HeroClass(models.Model):
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Hero's classes"


class HeroRank(models.Model):
    value = models.IntegerField(unique=True)
    multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.value)

    class Meta:
        verbose_name_plural = "Hero's ranks"


class HeroRarity(models.Model):
    name = models.CharField(max_length=255)
    multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Hero's rarities"


# Create your models here.
class HeroType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image_url = models.URLField(blank=True, null=True)
    # base_int = models.IntegerField(default=1)
    # base_agi = models.IntegerField(default=1)
    # base_str = models.IntegerField(default=1)

    hp_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    atk_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    matk_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    def_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    aspd_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1)

    hero_class = models.ForeignKey(
        HeroClass,
        on_delete=models.CASCADE,
        default=1,
        related_name="heroes",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Hero's types"


def default_gem_slot_dict():
    return {
        "slot1": None,
        "slot2": None,
        "slot3": None,
        "slot4": None,
        "slot5": None,
    }


class HeroInfo(models.Model):
    nft_id = models.CharField(max_length=255, unique=True)
    # move team slot to player
    # team_slot = models.IntegerField(default=0)
    exp = models.IntegerField(default=0)
    rarity = models.ForeignKey(
        HeroRarity,
        on_delete=models.CASCADE,
        related_name="heroes_rarity",
        null=True,
        blank=True,
    )
    hero_type = models.ForeignKey(
        HeroType,
        on_delete=models.CASCADE,
        related_name="heroes_type",
        null=True,
        blank=True,
    )
    rank = models.ForeignKey(
        HeroRank,
        on_delete=models.CASCADE,
        related_name="heroes_rank",
        null=True,
        blank=True,
        to_field="value",
    )
    owner = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Hero's info"

    def __str__(self):
        return self.nft_id

    # @property
    # def base_hero(self):
    #     try:
    #         return HeroOnChain.objects.get(nft_id=self.nft_id)
    #     except HeroOnChain.DoesNotExist:
    #         try:
    #             return HeroOffChain.objects.get(nft_id=self.nft_id)
    #         except HeroOffChain.DoesNotExist:
    #             return None

    def remove_equip_gem(self):
        GemUser.objects.filter(hero=self).delete()

    @property
    def level(self) -> int:
        _level = 1
        _exp = self.exp
        _i = 0
        _require = 100
        while _exp >= _require:
            _exp -= 100 * (1.2 ** _i)
            _level += 1
            _i += 1
            _require = 100 * (1.2 ** _i)
        return _level

    @property
    def current_exp(self) -> int:
        _exp = self.exp
        _i = 0
        _require = 100
        while _exp >= _require:
            _exp -= 100 * (1.2 ** _i)
            _i += 1
            _require = 100 * (1.2 ** _i)
        return _exp

    @property
    def need_exp(self) -> int:
        _exp = self.exp
        _i = 0
        _require = 100
        while _exp >= _require:
            _exp -= 100 * (1.2 ** _i)
            _i += 1
            _require = 100 * (1.2 ** _i)
        return _require

    @cached_property
    def hero_user(self):
        return HeroUser.objects.get(info=self.nft_id)

    @cached_property
    def base_str(self):
        return self.hero_user.base_str

    @cached_property
    def base_agi(self):
        return self.hero_user.base_agi

    @cached_property
    def base_vit(self):
        return self.hero_user.base_vit

    @cached_property
    def base_int(self):
        return self.hero_user.base_int

    @cached_property
    def equip_gems(self):
        return GemUser.objects.filter(hero_id=self)

    def gem_str(self, _stat):
        equip_gem = self.equip_gems
        stat_plus = 0
        for gem_user in equip_gem:
            if gem_user.gem is None:
                continue
            if gem_user.gem.attribute.id == 1:
                stat_plus += gem_user.gem.attribute_value
        return _stat + stat_plus

    def gem_agi(self, _stat):
        equip_gem = self.equip_gems
        stat_plus = 0
        for gem_user in equip_gem:
            if gem_user.gem is None:
                continue
            if gem_user.gem.attribute.id == 5:
                stat_plus += gem_user.gem.attribute_value
        return _stat + stat_plus

    def gem_vit(self, _stat):
        equip_gem = self.equip_gems
        stat_plus = 0
        for gem_user in equip_gem:
            if gem_user.gem is None:
                continue
            if gem_user.gem.attribute.id == 6:
                stat_plus += gem_user.gem.attribute_value
        return _stat + stat_plus

    def gem_int(self, _stat):
        equip_gem = self.equip_gems
        stat_plus = 0
        for gem_user in equip_gem:
            if gem_user.gem is None:
                continue
            if gem_user.gem.attribute.id == 7:
                stat_plus += gem_user.gem.attribute_value
        return _stat + stat_plus

    # @property
    # def rarity(self):
    #     hex_value = int(self.nft_id.nft_id, 16)
    #     this_rarity = uint8(hex_value >> 64).value & 0xFF
    #     return HeroRarity.objects.get(id=this_rarity)
    # @property
    # def hero(self) -> Hero:
    #     hex_value = int(self.nft_id.nft_id, 16)
    #     this_hero = uint16(hex_value >> (64 + 8 + 8)).value & 0xFFFF
    #     return Hero.objects.get(id=this_hero)

    @property
    def calculated_str(self) -> int:
        base_str = self.base_str
        level = self.level
        rank_value = self.rank.value
        rank_multiplier = self.rank.multiplier
        rarity_multiplier = self.rarity.multiplier
        str_value = (
                (base_str + ((level - 1) * 2))
                * (rank_multiplier ** rank_value)
                * rarity_multiplier
        )
        str_value = self.gem_str(str_value)
        return round(str_value)

    @property
    def calculated_agi(self) -> int:
        base_agi = self.base_agi
        level = self.level
        rank_value = self.rank.value
        rank_multiplier = self.rank.multiplier
        rarity_multiplier = self.rarity.multiplier
        agi_value = (
                (base_agi + ((level - 1) * 2))
                * (rank_multiplier ** rank_value)
                * rarity_multiplier
        )
        agi_value = self.gem_agi(agi_value)
        return round(agi_value)

    @property
    def calculated_vit(self) -> int:
        base_vit = self.base_vit
        level = self.level
        rank_value = self.rank.value
        rank_multiplier = self.rank.multiplier
        rarity_multiplier = self.rarity.multiplier
        vit_value = (
                (base_vit + ((level - 1) * 2))
                * (rank_multiplier ** rank_value)
                * rarity_multiplier
        )
        vit_value = self.gem_vit(vit_value)
        return round(vit_value)

    @property
    def calculated_int(self) -> int:
        base_int = self.base_int
        level = self.level
        rank_value = self.rank.value
        rank_multiplier = self.rank.multiplier
        rarity_multiplier = self.rarity.multiplier
        int_value = (
                (base_int + ((level - 1) * 2))
                * (rank_multiplier ** rank_value)
                * rarity_multiplier
        )
        int_value = self.gem_int(int_value)
        return round(int_value)

    @property
    def calculated_hp(self) -> int:
        base_hp = 100
        level = self.level
        hp_multiplier = self.hero_type.hp_multiplier
        hp_value = (base_hp + (level * 10) + (self.calculated_vit * 10)) * hp_multiplier
        return round(hp_value)

    @property
    def calculated_atk(self) -> int:
        base_atk = 10
        level = self.level
        atk_multiplier = self.hero_type.atk_multiplier
        atk_value = (
                            base_atk + (level * 10) + (self.calculated_str * 2)
                    ) * atk_multiplier
        return round(atk_value)

    @property
    def calculated_matk(self) -> int:
        base_matk = 10
        level = self.level
        matk_multiplier = self.hero_type.matk_multiplier
        matk_value = (
                             base_matk + (level * 10) + (self.calculated_int * 2)
                     ) * matk_multiplier
        return round(matk_value)

    @property
    def calculated_def(self) -> int:
        base_def = 10
        level = self.level
        def_multiplier = self.hero_type.def_multiplier
        def_value = (
                            base_def + (level * 10) + (self.calculated_vit * 2)
                    ) * def_multiplier
        return round(def_value)

    @property
    def calculated_aspd(self) -> int:
        base_aspd = 100
        level = self.level
        aspd_multiplier = self.hero_type.aspd_multiplier
        aspd_value = base_aspd + ((((1 * level) + self.calculated_agi) * 2 ) * aspd_multiplier)
        return round(aspd_value)

    # @property
    # def rarity(self):
    #     hex_value = int(self.nft_id.nft_id, 16)
    #     this_rarity = uint8(hex_value >> 64).value & 0xFF
    #     return HeroRarity.objects.get(id=this_rarity)
    # @property
    # def hero(self) -> Hero:
    #     hex_value = int(self.nft_id.nft_id, 16)
    #     this_hero = uint16(hex_value >> (64 + 8 + 8)).value & 0xFFFF
    #     return Hero.objects.get(id=this_hero)


class HeroUser(models.Model):
    info = models.OneToOneField(
        HeroInfo,
        on_delete=models.CASCADE,
        primary_key=True,
        max_length=255,
        db_column="id",
        to_field="nft_id",
        blank=True,
    )
    base_str = models.IntegerField(db_column="str")
    base_int = models.IntegerField(db_column="int")
    base_vit = models.IntegerField(db_column="vit")
    base_agi = models.IntegerField(db_column="agi")
    rank = models.ForeignKey(
        HeroRank,
        on_delete=models.CASCADE,
        related_name="onchain_this_rank",
        default=0,
        blank=True,
        null=True,
        db_column="rank",
        to_field="value",
    )  # rarity
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        to_field="username",
        blank=True,
        null=True,
        db_column="owner",
    )
    is_on_chain = models.BooleanField(
        db_column="isOnChain"
    )  # Field name made lowercase.
    is_deleted = models.BooleanField(
        db_column="isDeleted"
    )  # Field name made lowercase.
    created_at = models.DateTimeField(
        db_column="createdAt"
    )  # Field name made lowercase.
    updated_at = models.DateTimeField(
        db_column="updatedAt"
    )  # Field name made lowercase.
    transferred_at = models.IntegerField(db_column="transferredAt")

    class Meta:
        managed = False
        db_table = "indexer_hero_stats"
        verbose_name_plural = "Individual heroes"

    def __str__(self) -> str:
        return str(self.pk)

    def delete(self, *args, **kwargs):
        return


class GemAttribute(models.Model):
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Gem's attributes"


class Gem(models.Model):
    name = models.CharField(max_length=255, unique=True)
    nft_id = models.CharField(max_length=255, default="", primary_key=True)

    attribute = models.ForeignKey(
        GemAttribute, on_delete=models.CASCADE, related_name="gems"
    )
    attribute_value = models.DecimalField(max_digits=8, decimal_places=2, default=1)
    attribute_is_percentage = models.BooleanField(default=False)
    level_needed = models.IntegerField(default=1)
    is_on_chain = models.BooleanField(default=True)
    price = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class GemUser(models.Model):
    gem = models.ForeignKey(Gem, on_delete=models.CASCADE, default=None, null=True)
    hero = models.ForeignKey(HeroInfo, on_delete=models.CASCADE, default='')

    slot = models.PositiveIntegerField(null=False, validators=[MinValueValidator(1)], default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # def __str__(self) -> str:
    #     # if self.hero is None:
    #     #     hero_nft = "None"
    #     # else:
    #     #     hero_nft = self.hero.nft_id
    #     return f"nft {self.gem.nft_id} user {self.user.username} hero {self.hero_nft_id} at slot {self.gem_slot}"

    class Meta:
        verbose_name_plural = "Individual gems"
        constraints = [
            models.UniqueConstraint(fields=['hero', 'slot'], name='hero_slot')
        ]
