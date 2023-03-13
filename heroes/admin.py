from django.contrib import admin

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


# Register your models here.
class MyAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "modified_at")


# class HeroesInline(admin.TabularInline):
#     model = HeroUser


# class MyHero(MyAdmin):
#     inlines = [HeroesInline]
class GemAttributeAdmin(MyAdmin):
    list_display = ["name"]


class GemAdmin(MyAdmin):
    list_display = [
        "name",
        "nft_id",
        "attribute",
        "attribute_value",
        "attribute_is_percentage",
        "level_needed",
        "is_on_chain",
        "price",
    ]


class GemUserAdmin(MyAdmin):
    list_display = ["gem", "hero", "slot"]


class HeroTypeAdmin(MyAdmin):
    list_display = [
        "name",
        "hero_class",
        "hp_multiplier",
        "atk_multiplier",
        "matk_multiplier",
        "def_multiplier",
        "aspd_multiplier",
    ]


class HeroUserAdmin(admin.ModelAdmin):
    list_display = [
        "info",
        "rank",
        "base_str",
        "base_int",
        "base_vit",
        "base_agi",
        "is_on_chain",
        "is_deleted",
    ]


class HeroInfoAdmin(MyAdmin):
    list_display = ["nft_id", "exp", "rarity", "hero_type", "rank", "owner"]


class HeroRarityAdmin(MyAdmin):
    list_display = ["id", "name", "multiplier"]


class HeroRankAdmin(MyAdmin):
    list_display = ["id", "value", "multiplier"]


class HeroClassAdmin(MyAdmin):
    list_display = ["id", "name"]


# class GemAttributeAdmin(MyAdmin):
#     list_display = ["name"]
# class GemAttributeAdmin(MyAdmin):
#     list_display = ["name"]
# class GemAttributeAdmin(MyAdmin):
#     list_display = ["name"]
# class GemAttributeAdmin(MyAdmin):
#     list_display = ["name"]
# class GemAttributeAdmin(MyAdmin):
#     list_display = ["name"]


admin.site.register(GemAttribute, GemAttributeAdmin)
admin.site.register(Gem, GemAdmin)
admin.site.register(GemUser, GemUserAdmin)
admin.site.register(HeroType, HeroTypeAdmin)
admin.site.register(HeroInfo, HeroInfoAdmin)
admin.site.register(HeroUser, HeroUserAdmin)
admin.site.register(HeroRarity, HeroRarityAdmin)
admin.site.register(HeroRank, HeroRankAdmin)
admin.site.register(HeroClass, HeroClassAdmin)
