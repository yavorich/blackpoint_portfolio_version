from django.contrib import admin
from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from core.unfold.admin import UnfoldModelAdmin
from core.unfold.filters import AllValuesFieldListDropdownFilter

from apps.vending.models import City, Place, SubscriptionTariff


@admin.register(City)
class CityAdmin(UnfoldModelAdmin):
    list_display = ["name"]


class PlaceModelForm(ModelForm):
    tariffs = ModelMultipleChoiceField(
        queryset=SubscriptionTariff.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Place
        fields = ["name", "city", "address", "tariffs", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Предустанавливаем все тарифы по умолчанию
        if not self.instance.pk:  # Только для новых объектов
            self.fields["tariffs"].initial = SubscriptionTariff.objects.all()


@admin.register(Place)
class PlaceAdmin(UnfoldModelAdmin):
    # form = PlaceModelForm
    list_display = ["name", "city", "address", "is_active"]
    list_filter = (("city__name", AllValuesFieldListDropdownFilter),)


@admin.register(SubscriptionTariff)
class SubscriptionTariffAdmin(UnfoldModelAdmin):
    list_display = ["name", "days", "cups", "price", "is_active"]

    def has_delete_permission(self, request, obj=...):
        return False
