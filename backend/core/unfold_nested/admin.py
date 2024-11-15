from nested_admin.nested import (
    NestedModelAdminMixin,
    NestedInlineModelAdminMixin,
    NestedTabularInlineMixin,
)
from unfold.admin import StackedInline, TabularInline

from core.unfold.admin import UnfoldModelAdmin


class UnfoldNestedAdmin(NestedModelAdminMixin, UnfoldModelAdmin):
    pass


class UnfoldNestedTabularInline(NestedTabularInlineMixin, TabularInline):
    template = "unfold/nested/tabular.html"


class UnfoldNestedStackedInline(NestedInlineModelAdminMixin, StackedInline):
    template = "unfold/nested/stacked.html"
