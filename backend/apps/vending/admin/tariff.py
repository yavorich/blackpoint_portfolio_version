from django.contrib import admin

from core.unfold.admin import UnfoldModelAdmin
from apps.vending.models import SubscriptionTariff


@admin.register(SubscriptionTariff)
class SubscriptionTariffAdmin(UnfoldModelAdmin):
    list_display = ["name", "days", "cups", "price", "is_active"]

    def has_delete_permission(self, request, obj=...):
        return False
