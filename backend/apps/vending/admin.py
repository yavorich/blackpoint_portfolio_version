from django.contrib import admin
from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple

from apps.vending.models import Place, SubscriptionTariff


class PlaceModelForm(ModelForm):
    tariffs = ModelMultipleChoiceField(
        queryset=SubscriptionTariff.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Place
        fields = ["address", "tariffs"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Предустанавливаем все тарифы по умолчанию
        if not self.instance.pk:  # Только для новых объектов
            self.fields["tariffs"].initial = SubscriptionTariff.objects.all()


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    form = PlaceModelForm


@admin.register(SubscriptionTariff)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["name", "days", "cups", "price"]
