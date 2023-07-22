from django.core.validators import RegexValidator
from django.db import models

from core.boilerplate.abstract_models import TemplateModel
from ecommerce_app.models import Shop
from inventory_app.constants import BookRegex
from user_app.models import UserAccount


class Item(TemplateModel):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    seller = models.ForeignKey(Shop, on_delete=models.CASCADE,
                               help_text="Delete shop's inventory when shop is deleted.")
    presentation = models.TextField(
        blank=True, null=True, help_text="Holds the html string to display the splash page for the item.")
    current_stock = models.PositiveIntegerField(default=1)
    minimum_stock = models.PositiveIntegerField(default=1)
    in_stock = models.BooleanField(default=False)
    active_listing = models.BooleanField(default=False)
    next_restock = models.DateTimeField(blank=True, null=True)
    last_restock = models.DateTimeField(blank=True, null=True)
    last_edited_by = models.ForeignKey(
        UserAccount, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        self.title = self.title.title()
        super(Item, self).save(*args, **kwargs)


class BookItemDetail(TemplateModel):
    book = models.ForeignKey(Item, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=16, blank=True, null=True)
    title = models.CharField(max_length=256)
    subtitle = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    published = models.CharField(
        validators=(
            RegexValidator(
                BookRegex.YEAR_REGEX
            ),
        ),
        max_length=4,
        blank=True,
        null=True
    )
    author = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        author = self.author if self.author else ""
        by_str = " by " if self.author else ""
        return f"{self.title}{by_str}{author}"

    def save(self, *args, **kwargs):

        self.title = self.title.title()

        if self.isbn:
            self.isbn = self.isbn.upper()
        if self.subtitle:
            self.subtitle = self.subtitle.title()
        if self.summary:
            self.summary = self.summary.encode(encoding="utf-8")

        super(BookItemDetail, self).save(*args, **kwargs)
