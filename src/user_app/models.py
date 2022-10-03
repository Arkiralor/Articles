from datetime import timedelta
from email.policy import default

from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import check_password
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone

from core.boilerplate.abstract_models import TemplateModel
from core.settings import OTP_EXPIRY_MINUTES
from user_app.constants import UserRegex
from user_app.model_choices import UserAccountChoice

import uuid


class UserAccount(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False
    )

    username = models.CharField(max_length=16, unique=True)
    slug = models.SlugField(max_length=255, blank=True, null=True)

    first_name = models.CharField(max_length=16, blank=True, null=True)
    middle_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=16, blank=True, null=True)

    email = models.EmailField(
        validators=(
            EmailValidator(
                message="Please enter a valid email address.",
                code="400"
            ),
        ),
        unique=True
    )
    password = models.CharField(max_length=512)
    mobile = models.CharField(
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
    account_type = models.CharField(
        max_length=25, choices=UserAccountChoice.TYPE_CHOICES, default=UserAccountChoice.user)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        self.email = self.email.lower()
        self.slug = slugify(self.username)

        if self.first_name:
            self.first_name = self.first_name.title()
        if self.middle_name:
            self.middle_name = self.middle_name.title()
        if self.last_name:
            self.last_name = self.last_name.title()

        if self.is_staff and not self.is_superuser:
            self.account_type = UserAccountChoice.staff
        elif self.is_superuser:
            self.account_type = UserAccountChoice.admin
        else:
            self.account_type = UserAccountChoice.user

        super(UserAccount, self).save(*args, **kwargs)

    def authorize_password(self, password: str = None):
        """
        Alternate model-method to authorize the user with a password.
        """
        return check_password(password=password, encoded=self.password)

    class Meta:
        verbose_name = "User Account"
        verbose_name_plural = "User Accounts"
        ordering = ("-date_joined", "-created")
        indexes = (
            models.Index(fields=("username",), db_tablespace="user_accounts"),
            models.Index(fields=("slug",), db_tablespace="user_accounts"),
            models.Index(fields=("email",), db_tablespace="user_accounts"),
            models.Index(fields=("mobile",), db_tablespace="user_accounts"),
            models.Index(fields=("first_name", "middle_name",
                         "last_name"), db_tablespace="user_accounts"),
            models.Index(fields=("last_name", "middle_name",
                         "first_name"), db_tablespace="user_accounts")
        )


class UserOTP(TemplateModel):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    otp = models.CharField(max_length=512)
    expiry = models.DateTimeField(blank=True, null=True)
    verified = models.BooleanField(
        default=False, help_text="Whether the OTP has been used to log into the system.")

    def __str__(self):
        return f"One-Time-Password for user '{self.user.email}' created on {self.created.date()} at {self.created.time()}."

    def save(self, *args, **kwargs):
        self.expiry = self.created + timedelta(minutes=OTP_EXPIRY_MINUTES)
        super(UserOTP, self).save(*args, **kwargs)

    def authenticate_otp(self, otp: str = None):
        return check_password(password=otp, encoded=self.otp)

    class Meta:
        verbose_name = "User One-Time-Password"
        verbose_name_plural = "User One-Time-Passwords"
        ordering = ("-created",)
        indexes = (
            models.Index(fields=("user",), db_tablespace="user_accounts"),
            models.Index(fields=("expiry",), db_tablespace="user_accounts"),
            models.Index(fields=("verified",), db_tablespace="user_accounts")
        )
