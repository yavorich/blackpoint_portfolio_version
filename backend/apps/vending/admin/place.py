from django.contrib import admin
from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
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
        fields = ["name", "city", "address", "drinks", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Предустанавливаем все напитки по умолчанию
        if not self.instance.pk:  # Только для новых объектов
            self.fields["drinks"].initial = DrinkVolume.objects.all()


@admin.register(Place)
class PlaceAdmin(UnfoldModelAdmin):
    form = PlaceModelForm
    list_display = ["name", "partner", "city", "address", "is_active"]
    list_filter = (
        ("city__name", AllValuesFieldListDropdownFilter),
        ("partner__name", AllValuesFieldListDropdownFilter),
    )
    inlines = [PlaceDrinkHistoryInline]
