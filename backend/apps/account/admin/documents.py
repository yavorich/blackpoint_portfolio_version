from django.contrib import admin
from core.unfold.admin import UnfoldModelAdmin

from apps.account.models import Document


@admin.register(Document)
class DocumentAdmin(UnfoldModelAdmin):
    list_display = ["get_type_display", "file"]

    @admin.display(description="Тип документа")
    def get_type_display(self, obj):
        return obj.get_type_display()
