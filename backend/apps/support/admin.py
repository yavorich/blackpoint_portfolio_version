from django.contrib import admin

from apps.support.models import SupportRequest


@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "message"]
