# Register your models here.
from django.contrib import admin

from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):

    search_fields = (
        "ticket_number",
        "member__name",
    )

    list_filter = (
        "status",
    )

    list_display = (
        "formatted_number",
        "member",
        "status",
        "created_at",
    )