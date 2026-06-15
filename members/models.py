# Create your models here.
from decimal import Decimal
from django.db import models


class Member(models.Model):

    name = models.CharField(
        max_length=255,
        db_index=True
    )

    wallet_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    phone_number = models.CharField(
        max_length=20,
        db_index=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name