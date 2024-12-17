from django.contrib import admin
from django.utils.safestring import mark_safe

from core.unfold_nested.admin import UnfoldNestedStackedInline, UnfoldNestedAdmin
from core.unfold.filters import AllValuesFieldListDropdownFilter

from apps.vending.models import Place, DrinkVolume, DrinkHistory, DrinkType


class PlaceDrinkHistoryInline(UnfoldNestedStackedInline):
    model = DrinkHistory
    fields = ["drink_name", "price", "user", "purchased_at"]
    readonly_fields = fields
    extra = 0


class PlaceDrinkVolumeInline(UnfoldNestedStackedInline):
    model = DrinkVolume
    fields = ["volume_ml", "price"]
    extra = 0


class PlaceDrinkMenuInline(UnfoldNestedStackedInline):
    model = DrinkType
    inlines = [PlaceDrinkVolumeInline]
    fields = ["name"]
    extra = 0


@admin.register(Place)
class PlaceAdmin(UnfoldNestedAdmin):
    list_display = ["name", "partner", "city", "address", "is_active"]
    fields = (
        "name",
        "terminal_id",
        "partner",
        "city",
        "address",
        "latitude",
        "longitude",
        "qr_code_image",
        "is_active",
    )
    readonly_fields = ("qr_code_image",)
    list_filter = (
        ("city__name", AllValuesFieldListDropdownFilter),
        ("partner__name", AllValuesFieldListDropdownFilter),
    )
    inlines = [PlaceDrinkMenuInline, PlaceDrinkHistoryInline]

    @admin.display(description="QR-код")
    def qr_code_image(self, obj: Place):
        if obj.qr_code:
            return mark_safe(f'<img src="{obj.qr_code.url}" width="30%" />')
        return "QR-код не создан"
