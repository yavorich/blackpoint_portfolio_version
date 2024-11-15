from django.contrib.admin import AllValuesFieldListFilter
from django.contrib.admin.utils import (
    get_last_value_from_parameters,
    reverse_field_path,
)
from django.contrib.admin.views.main import ChangeList
from django.core.exceptions import FieldDoesNotExist
from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import ValueMixin, DropdownMixin


class AllValuesFieldListDropdownFilter(
    ValueMixin, DropdownMixin, AllValuesFieldListFilter
):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = field_path
        self.lookup_kwarg_isnull = "%s__isnull" % field_path
        self.lookup_val = params.get(self.lookup_kwarg)
        self.lookup_val_isnull = get_last_value_from_parameters(
            params, self.lookup_kwarg_isnull
        )
        self.empty_value_display = model_admin.get_empty_value_display()
        try:
            parent_model, reverse_path = reverse_field_path(model, field_path)
        except FieldDoesNotExist:
            parent_model = model
        # Obey parent ModelAdmin queryset when deciding which options to show
        if model == parent_model:
            queryset = model_admin.get_queryset(request)
        else:
            queryset = parent_model._default_manager.all()
        self.lookup_choices = (
            queryset.distinct().order_by(field.name).values_list(field.name, flat=True)
        )
        super(AllValuesFieldListFilter, self).__init__(
            field, request, params, model, model_admin, field_path
        )

    def choices(self, changelist: ChangeList):
        choices = [
            self.all_option,
            *[(val, self.get_display_value(val)) for val in self.lookup_choices],
        ]

        yield {
            "form": self.form_class(
                label=self.title,
                name=self.lookup_kwarg,
                choices=choices,
                data={self.lookup_kwarg: self.value()},
                multiple=self.multiple if hasattr(self, "multiple") else False,
            ),
        }

    @staticmethod
    def get_display_value(val):
        if isinstance(val, bool):
            return _("Yes") if val else _("No")
        elif val is None:
            return "---"
        return val
