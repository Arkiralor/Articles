from django.core.validators import EmailValidator, RegexValidator
from django.db import models

from core.boilerplate.abstract_models import TemplateModel
from user_app.models import UserAccount
from user_app.constants import UserRegex

class Shop(TemplateModel):
    name = models.CharField(max_length=128, unique=True)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    contact_email = models.EmailField(
        validators = (
            EmailValidator(
                message="Please enter a valid email address.",
                code="400"
            ),
        ),
        unique=True
    )
    contact_number = models.CharField(
        max_length=10,
        validators=(
            RegexValidator(
                regex=UserRegex.PHONE_REGEX,
                message="Please enter a phone number without the ISD code.",
                code="400"
            ),
        ),
        unique=True
    )
    presentation = models.TextField(
        blank=True, null=True, help_text="Holds the html string to display the splash page for the shop.")
    profile_picture = models.ImageField(upload_to='models/shops/profile_pictures/', blank=True, null=True)
    banner = models.ImageField(upload_to='models/shops/banners/', blank=True, null=True)
    logo = models.ImageField(upload_to='models/shops/logos/', blank=True, null=True)
    watermark = models.ImageField(upload_to='models/shops/watermarks/', blank=True, null=True)


class ShopExecutive(TemplateModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    executive = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    
