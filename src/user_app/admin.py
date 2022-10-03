from django.contrib import admin

from user_app.models import UserAccount, UserOTP


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "account_type", "last_login")
    ordering = ("-created",)


@admin.register(UserOTP)
class UserOTPAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "expiry", "verified")
    raw_id_fields = ("user",)
    ordering = ("-created",)
