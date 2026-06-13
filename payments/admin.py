from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    search_fields = ("bank_reference", "member__name")
    list_filter   = ("status", "event")
    list_display  = ("bank_reference", "member", "amount", "status", "event", "created_at")
