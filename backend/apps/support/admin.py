from django.contrib import admin
from core.unfold.admin import UnfoldModelAdmin

from apps.support.models import SupportRequest


@admin.register(SupportRequest)
class SupportRequestAdmin(UnfoldModelAdmin):
    list_display = ["id", "user", "message"]
