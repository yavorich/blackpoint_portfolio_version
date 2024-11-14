from django.contrib import admin

from apps.account.models import User, UserSubscription
from core.user_admin.mixins import ChangePasswordMixin


class UserSubscriptionInline(admin.TabularInline):
    model = UserSubscription
    fields = ["place", "expire_date"]
    extra = 0


@admin.register(User)
class UserAdmin(ChangePasswordMixin, admin.ModelAdmin):
    inlines = [UserSubscriptionInline]
    fieldsets = (
        (
            "Авторизация",
            {
                "fields": (
                    "username",
                    "password",
                    "uuid",
                )
            },
        ),
        (
            "Личные данные",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "avatar",
                )
            },
        ),
        (
            "Телеграм",
            {"fields": ("telegram_id",)},
        ),
        (
            "Разрешения",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "date_joined",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            "Авторизация",
            {
                # "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
        (
            "Разрешения",
            {"fields": ("is_active", "is_staff")},
        ),
    )
    readonly_fields = (
        "date_joined",
        "uuid",
    )
    list_display = (
        "id",
        "username",
        "telegram_id",
        "is_active",
        "is_staff",
    )
    list_display_links = ("id", "username")
    list_filter = (
        "is_active",
        "is_staff",
    )
    search_fields = (
        "username",
        "telegram_id",
    )
    filter_horizontal = ()
    ordering = ("-date_joined",)
