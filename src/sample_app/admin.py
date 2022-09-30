from django.contrib import admin
from sample_app.models import SampleModel


@admin.register(SampleModel)
class SampleModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "char_field",
        "decimal_field",
        "integer_field",
        "boolean_field"
    )
    search_fields = ("name", "char_field")
    ordering = (
        "name",
        "-created"
    )
