# Register your models here.
from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    search_fields = (
        "mpesa_reference",
        "member__name",
    )

    list_filter = (
        "status",
    )

    list_display = (
        "mpesa_reference",
        "member",
        "amount",
        "status",
        "created_at",
    )