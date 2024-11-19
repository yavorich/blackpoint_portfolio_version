from django.contrib import admin
from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from django.utils.safestring import mark_safe
from unfold.admin import StackedInline

from core.unfold.admin import UnfoldModelAdmin
from core.unfold.filters import AllValuesFieldListDropdownFilter

from apps.vending.models import Place, DrinkVolume, DrinkHistory


class PlaceDrinkHistoryInline(StackedInline):
    model = DrinkHistory
    fields = ["drink", "user", "purchased_at"]
    readonly_fields = fields
    extra = 0


class PlaceModelForm(ModelForm):
    drinks = ModelMultipleChoiceField(
        queryset=DrinkVolume.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
        label="Меню",
    )

    class Meta:
        model = Place
        fields = ["name", "partner", "city", "address", "drinks", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Предустанавливаем все напитки по умолчанию
        if not self.instance.pk:  # Только для новых объектов
            self.fields["drinks"].initial = DrinkVolume.objects.all()


@admin.register(Place)
class PlaceAdmin(UnfoldModelAdmin):
    form = PlaceModelForm
    list_display = ["name", "partner", "city", "address", "is_active"]
    fields = (
        "name",
        "partner",
        "city",
        "address",
        "drinks",
        "qr_code_image",
        "is_active",
    )
    readonly_fields = ("qr_code_image",)
    list_filter = (
        ("city__name", AllValuesFieldListDropdownFilter),
        ("partner__name", AllValuesFieldListDropdownFilter),
    )
    inlines = [PlaceDrinkHistoryInline]

    @admin.display(description="QR-код")
    def qr_code_image(self, obj: Place):
        if obj.qr_code:
            return mark_safe(f'<img src="{obj.qr_code.url}" width="30%" />')
        return "QR-код не создан"
