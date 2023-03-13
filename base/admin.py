from django.contrib import admin

from .models import Color, Fruit


# Register your models here.
class MyAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "modified_at")


# admin.site.register(Fruit, MyAdmin)
# admin.site.register(Color, MyAdmin)
