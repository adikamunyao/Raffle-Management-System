from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Prize
from .models import Winner


@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "position",
        "quantity",
        "event",
        "active",
    )

    list_filter = (
        "event",
        "active",
    )


@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):

    list_display = (
        "ticket",
        "prize",
        "event",
        "created_at",
    )

    list_filter = (
        "event",
    )