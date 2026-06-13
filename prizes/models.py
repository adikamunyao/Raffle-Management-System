# Create your models here.
from django.db import models
from events.models import RaffleEvent

# Prizes App Models
class Prize(models.Model):

    event = models.ForeignKey(
        RaffleEvent,
        on_delete=models.CASCADE,
        related_name="prizes"
    )

    position = models.PositiveIntegerField()

    name = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            "position",
            "name"
        ]

    def __str__(self):
        return self.name

# Winner Model    
class Winner(models.Model):

    event = models.ForeignKey(
        RaffleEvent,
        on_delete=models.CASCADE,
        related_name="winners"
    )

    prize = models.ForeignKey(
        Prize,
        on_delete=models.PROTECT,
        related_name="winners"
    )

    ticket = models.ForeignKey(
        "tickets.Ticket",
        on_delete=models.PROTECT,
        related_name="wins"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "prize",
                    "ticket"
                ],
                name="unique_prize_ticket"
            )
        ]

    def __str__(self):

        return (
            f"{self.ticket} "
            f"- "
            f"{self.prize.name}"
        )