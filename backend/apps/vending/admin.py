from django.contrib import admin

from apps.vending.models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    pass
