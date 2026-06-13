# Create your models here.
from django.db import models

from members.models import Member
from payments.models import Payment
from events.models import RaffleEvent


class Ticket(models.Model):

    GENERATED = "GENERATED"
    PRINTED = "PRINTED"
    COLLECTED = "COLLECTED"
    WON = "WON"

    STATUS_CHOICES = [
        (GENERATED, "Generated"),
        (PRINTED, "Printed"),
        (COLLECTED, "Collected"),
        (WON, "Won"),
    ]

    event = models.ForeignKey(
        "events.RaffleEvent",
        on_delete=models.PROTECT,
        related_name="tickets"
    )

    ticket_number = models.PositiveIntegerField()

    member = models.ForeignKey(
        "members.Member",
        on_delete=models.PROTECT,
        related_name="tickets"
    )

    payment = models.ForeignKey(
        "payments.Payment",
        on_delete=models.PROTECT,
        related_name="tickets"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=GENERATED
    )

    printed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    collected_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event", "ticket_number"],
                name="unique_ticket_per_event"
            )
        ]

    @property
    def formatted_number(self):
        return f"{self.ticket_number:04d}"