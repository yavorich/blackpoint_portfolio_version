from django.contrib import admin
from django.contrib.auth.models import Group
from core.unfold_nested.admin import (
    UnfoldNestedAdmin,
    UnfoldNestedTabularInline,
    UnfoldNestedStackedInline,
)

from apps.account.models import User, UserSubscription, SubscriptionPayment
from core.unfold_user_admin.mixins import ChangePasswordMixin
from core.unfold.admin import UnfoldModelAdmin
from core.unfold.filters import AllValuesFieldListDropdownFilter


@admin.register(SubscriptionPayment)
class SubscriptionPaymentAdmin(UnfoldModelAdmin):
    list_display = ["payment_date", "price", "user", "tariff", "place"]
    list_filter = (
        ("user__username", AllValuesFieldListDropdownFilter),
        ("tariff__name", AllValuesFieldListDropdownFilter),
        ("place__address", AllValuesFieldListDropdownFilter),
    )
    date_hierarchy = "payment_date"


class SubscriptionPaymentInline(UnfoldNestedTabularInline):
    model = SubscriptionPayment
    fields = ["payment_date", "price"]
    extra = 0


class UserSubscriptionInline(UnfoldNestedStackedInline):
    model = UserSubscription
    inlines = [SubscriptionPaymentInline]
    fields = [
        "tariff_name",
        "start_date",
        "expire_date",
        "place_address",
    ]
    readonly_fields = fields
    extra = 0

    @admin.display(description="Название")
    def tariff_name(self, obj):
        return obj.tariff.name

    @admin.display(description="Адрес автомата")
    def place_address(self, obj):
        return obj.place.address

    @admin.display(description="Стоимость")
    def tariff_price(self, obj):
        return obj.tariff.price


@admin.register(User)
class UserAdmin(ChangePasswordMixin, UnfoldNestedAdmin):
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
        ("is_active", AllValuesFieldListDropdownFilter),
        ("is_staff", AllValuesFieldListDropdownFilter),
    )
    search_fields = (
        "username",
        "telegram_id",
    )
    filter_horizontal = ()
    ordering = ("-date_joined",)


admin.site.unregister(Group)
