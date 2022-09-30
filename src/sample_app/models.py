from django.db import models
from core.boilerplate.abstract_models import TemplateModel


class SampleModel(TemplateModel):
    name = models.CharField(max_length=16)
    char_field = models.CharField(max_length=128, blank=True, null=True)
    decimal_field = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    integer_field = models.PositiveIntegerField(blank=True, null=True)
    boolean_field = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.char_field = self.char_field.lower()

        if self.integer_field and self.integer_field > 25:
            self.boolean_field = True

        super(SampleModel, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            "name",
            "char_field",
            "decimal_field",
            "integer_field",
            "boolean_field"
        )
        verbose_name = "Sample Object"
        verbose_name_plural = "Sample Objects"
        ordering = (
            "name",
            "-created"
        )
