from django.contrib import admin

from .models import Stage


# Register your models here.
class MyAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "modified_at")


admin.site.register(Stage, MyAdmin)
