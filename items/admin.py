from django.contrib import admin

# from .models import Color, Fruit


# Register your models here.
class MyAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "modified_at")
