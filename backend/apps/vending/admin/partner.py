from django.contrib import admin

from core.unfold.admin import UnfoldModelAdmin
from apps.vending.models import Partner


@admin.register(Partner)
class PartnerAdmin(UnfoldModelAdmin):
    list_display = ["name"]
