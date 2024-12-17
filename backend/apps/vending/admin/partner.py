from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.db.models import Sum
from django.utils.timezone import now, timedelta

from core.unfold.admin import UnfoldModelAdmin
from unfold.admin import TabularInline
from apps.account.models import SubscriptionPayment
from apps.vending.models import Partner, DrinkHistory


class TotalStatisticFormSet(BaseInlineFormSet):
    def get_queryset(self):
        queryset = super().get_queryset()
        return list(queryset) + [self.model(**self.get_total_model_kwargs(queryset))]

    @staticmethod
    def get_total_model_kwargs(queryset):
        return {}


class TotalStatisticInlineMixin:
    empty_str = ""
    total_str = "Итого"

    def has_change_permission(self, request, obj=None):
        return False

    @staticmethod
    def is_total_obj(obj):
        return obj.pk is None


class DrinkHistoryFormSet(TotalStatisticFormSet):
    @staticmethod
    def get_total_model_kwargs(queryset):
        return {
            "place": None,
            "user": None,
            "drink_name": None,
            "price": queryset.aggregate(total=Sum("price"))["total"] or 0,
            "purchased_at": None,
        }


class SubscriptionPaymentFormSet(TotalStatisticFormSet):
    @staticmethod
    def get_total_model_kwargs(queryset):
        return {
            "place": None,
            "user": None,
            "tariff": None,
            "price": queryset.aggregate(total=Sum("price"))["total"] or 0,
            "payment_date": None,
        }


class PartnerDrinkHistoryInline(TotalStatisticInlineMixin, TabularInline):
    model = DrinkHistory
    formset = DrinkHistoryFormSet
    can_delete = False
    max_num = 0
    fields = ["place", "user", "drink_name", "get_purchased_at", "price"]
    readonly_fields = fields
    extra = 0

    def get_empty_value_display(self):
        return " "

    def get_purchased_at(self, obj: DrinkHistory):
        if self.is_total_obj(obj):
            return self.total_str
        return obj.purchased_at.strftime("%d.%m.%Y")

    get_purchased_at.short_description = "Дата покупки"

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Получаем параметры фильтрации из GET-запроса
        filter_type = request.GET.get("filter_type")
        date_from = request.GET.get("date_from")
        date_to = request.GET.get("date_to")

        # Фильтруем queryset по типу фильтрации
        if filter_type == "week":
            qs = qs.filter(purchased_at__gte=now() - timedelta(weeks=1))
        elif filter_type == "month":
            qs = qs.filter(purchased_at__gte=now() - timedelta(days=30))
        elif filter_type == "3_months":
            qs = qs.filter(purchased_at__gte=now() - timedelta(days=90))
        elif filter_type == "total":
            pass  # Отображаем всё
        elif date_from and date_to:
            qs = qs.filter(purchased_at__range=[date_from, date_to])

        return qs


class PartnerSubscriptionPaymentInline(TotalStatisticInlineMixin, TabularInline):
    model = SubscriptionPayment
    formset = SubscriptionPaymentFormSet
    fields = ["place", "user", "tariff", "get_payment_date", "price"]
    readonly_fields = fields
    can_delete = False
    max_num = 0
    extra = 0

    def get_empty_value_display(self):
        return " "

    def get_payment_date(self, obj):
        if self.is_total_obj(obj):
            return self.total_str
        return obj.payment_date.strftime("%d.%m.%Y")

    get_payment_date.short_description = "Дата покупки"

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Получаем параметры фильтрации из GET-запроса
        filter_type = request.GET.get("filter_type")
        date_from = request.GET.get("date_from")
        date_to = request.GET.get("date_to")

        # Фильтруем queryset по типу фильтрации
        if filter_type == "week":
            qs = qs.filter(payment_date__gte=now() - timedelta(weeks=1))
        elif filter_type == "month":
            qs = qs.filter(payment_date__gte=now() - timedelta(days=30))
        elif filter_type == "3_months":
            qs = qs.filter(payment_date__gte=now() - timedelta(days=90))
        elif filter_type == "total":
            pass  # Отображаем всё
        elif date_from and date_to:
            qs = qs.filter(payment_date__range=[date_from, date_to])

        return qs


@admin.register(Partner)
class PartnerAdmin(UnfoldModelAdmin):
    list_display = ["name"]
    inlines = [PartnerDrinkHistoryInline, PartnerSubscriptionPaymentInline]
    change_form_template = "date_filter_change_form.html"

    class Media:
        css = {"all": ("remove_inline_subtitles.css",)}

    def change_view(self, request, object_id, form_url="", extra_context=None):
        # Передача дополнительных данных в шаблон
        extra_context = extra_context or {}
        extra_context["filter_type"] = request.GET.get("filter_type", "total")
        extra_context["date_from"] = request.GET.get("date_from", "")
        extra_context["date_to"] = request.GET.get("date_to", "")
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Фильтрация будет происходить на уровне inlines, а не основного списка.
        return queryset
