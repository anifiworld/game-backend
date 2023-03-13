from django.contrib import admin

# Register your models here.
from .models import ItemBalance


class ItemBalanceAdmin(admin.ModelAdmin):
    list_display = ["address", "resource", "balance", "expiration_date", "is_on_chain"]

admin.site.register(ItemBalance, ItemBalanceAdmin)
