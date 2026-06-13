# Register your models here.
from django.contrib import admin

from .models import RaffleEvent


@admin.register(RaffleEvent)
class RaffleEventAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "ticket_price",
        "draw_date",
        "status",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }