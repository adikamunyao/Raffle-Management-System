# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        (
            "Raffle Permissions",
            {
                "fields": (
                    "role",
                )
            },
        ),
    )

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "role",
        "is_active",
    )

    list_filter = (
        "role",
        "is_active",
    )