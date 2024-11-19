from django.contrib import admin
from django.contrib.auth.models import Group
from core.unfold_nested.admin import (
    UnfoldNestedAdmin,
    UnfoldNestedTabularInline,
    UnfoldNestedStackedInline,
)

from apps.account.models import User, UserSubscription, SubscriptionPayment
from apps.vending.models import DrinkHistory
from core.unfold_user_admin.mixins import ChangePasswordMixin
from core.unfold.admin import UnfoldModelAdmin
from core.unfold.filters import AllValuesFieldListDropdownFilter


@admin.register(SubscriptionPayment)
class SubscriptionPaymentAdmin(UnfoldModelAdmin):
    list_display = [
        "uuid",
        "payment_date",
        "price",
        "user",
        "tariff",
        "address",
        "partner_name",
    ]
    list_filter = (
        ("user__username", AllValuesFieldListDropdownFilter),
        ("tariff__name", AllValuesFieldListDropdownFilter),
        ("place__address", AllValuesFieldListDropdownFilter),
        ("place__partner__name", AllValuesFieldListDropdownFilter),
    )
    date_hierarchy = "payment_date"

    @admin.display(description="Адрес автомата")
    def address(self, obj: SubscriptionPayment):
        return obj.place.address if obj.place else None

    @admin.display(description="Наименование партнёра автомата")
    def partner_name(self, obj: SubscriptionPayment):
        partner = obj.place.partner if obj.place else None
        return partner.name if partner else None


class SubscriptionPaymentInline(UnfoldNestedTabularInline):
    model = SubscriptionPayment
    fields = ["payment_date", "price"]
    readonly_fields = fields
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


class UserDrinkHistoryInline(UnfoldNestedStackedInline):
    model = DrinkHistory
    fields = ["place", "drink", "purchased_at"]
    readonly_fields = fields
    extra = 0


@admin.register(User)
class UserAdmin(ChangePasswordMixin, UnfoldNestedAdmin):
    inlines = [UserSubscriptionInline, UserDrinkHistoryInline]
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
