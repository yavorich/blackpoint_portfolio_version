from django.contrib import admin

from core.unfold.admin import UnfoldModelAdmin
from apps.vending.models import City


@admin.register(City)
class CityAdmin(UnfoldModelAdmin):
    list_display = ["name"]
