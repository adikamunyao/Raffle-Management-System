from decimal import Decimal
from django.db import models
from members.models import Member
from events.models import RaffleEvent


class Payment(models.Model):

    PENDING  = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"

    STATUS_CHOICES = [
        (PENDING,  "Pending"),
        (VERIFIED, "Verified"),
        (REJECTED, "Rejected"),
    ]

    member = models.ForeignKey(
        Member, on_delete=models.PROTECT, related_name="payments"
    )

    bank_reference = models.CharField(
        max_length=30, unique=True, db_index=True
    )

    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )

    sms_text = models.TextField()

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=PENDING
    )

    processed_by = models.ForeignKey(
        "accounts.User", on_delete=models.PROTECT, null=True, blank=True
    )

    event = models.ForeignKey(
        RaffleEvent, on_delete=models.PROTECT, related_name="payments"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def tickets_generated(self):
        return self.tickets.exists()

    def __str__(self):
        return self.bank_reference


class WalletTransaction(models.Model):

    CREDIT = "CREDIT"
    DEBIT = "DEBIT"

    TRANSACTION_TYPE_CHOICES = [
        (CREDIT, "Credit"),
        (DEBIT, "Debit"),
    ]

    member = models.ForeignKey(
        Member,
        on_delete=models.PROTECT,
        related_name="wallet_transactions"
    )

    event = models.ForeignKey(
        RaffleEvent,
        on_delete=models.PROTECT,
        related_name="wallet_transactions",
        null=True,
        blank=True
    )

    payment = models.ForeignKey(
        Payment,
        on_delete=models.SET_NULL,
        related_name="wallet_transactions",
        null=True,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPE_CHOICES,
    )

    description = models.CharField(
        max_length=255,
        blank=True,
    )

    balance_after = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.member} {self.transaction_type} {self.amount}"
