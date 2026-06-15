from django.contrib import admin
from .models import Payment, WalletTransaction


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    search_fields = ("bank_reference", "member__name")
    list_filter   = ("status", "event")
    list_display  = ("bank_reference", "member", "amount", "status", "event", "created_at")


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    search_fields = ("member__name", "payment__bank_reference")
    list_filter = ("transaction_type", "event")
    list_display = ("member", "transaction_type", "amount", "balance_after", "event", "payment", "created_at")
