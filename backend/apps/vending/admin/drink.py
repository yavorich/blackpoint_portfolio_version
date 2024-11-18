from django.contrib import admin
from core.unfold.admin import UnfoldModelAdmin
from unfold.admin import TabularInline

from apps.vending.models import DrinkType, DrinkVolume


class DrinkVolumeInline(TabularInline):
    model = DrinkVolume
    fields = ["volume_ml", "price"]
    extra = 0


@admin.register(DrinkType)
class DrinkAdmin(UnfoldModelAdmin):
    list_display = ["name"]
    inlines = [DrinkVolumeInline]
