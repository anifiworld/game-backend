from django.contrib import admin

from .models import Player


# Register your models here.
class MyAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "coin_pending",
        "gold",
        # "coin_last_withdrawn",
        # "hero_slot5_expired",
        # "hero_slot5_max_lv",
        # "gem_slot5_expired",
        # "gem_slot5_max_lv",
        "stamina_last_updated_value",
        # "stamina_last_updated",
        "team_slot",
        # "created_at",
        # "modified_at",
        "is_banned",
    ]
    readonly_fields = ("created_at", "modified_at")


admin.site.register(Player, MyAdmin)
