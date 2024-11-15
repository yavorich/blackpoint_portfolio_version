from unfold.admin import ModelAdmin


class UnfoldModelAdmin(ModelAdmin):
    compressed_fields = True
    list_filter_submit = True
