from django.contrib import admin, messages
from core.unfold.admin import UnfoldModelAdmin
from apps.vending.models import VendistaAccount


@admin.register(VendistaAccount)
class VendistaAccountAdmin(UnfoldModelAdmin):
    list_display = ["login"]
    fields = ["login", "password"]
    actions = ["load_terminals"]

    @admin.action(description="Загрузить данные автоматов")
    def load_terminals(self, request, queryset):
        for obj in queryset:
            obj.get_terminals()

    def message_user(
        self, request, message, level=..., extra_tags=..., fail_silently=...
    ):
        pass

    def save_model(self, request, obj, form, change):
        if not obj.token:
            try:
                obj.token = obj.get_auth_token()
                super().save_model(request, obj, form, change)
                messages.success(request, "Аккаунт успешно добавлен")
            except Exception as e:
                messages.error(request, e)
