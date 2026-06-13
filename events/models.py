from decimal import Decimal
from django.db import models
from django.utils.text import slugify


class RaffleEvent(models.Model):

    DRAFT     = "DRAFT"
    ACTIVE    = "ACTIVE"
    CLOSED    = "CLOSED"
    COMPLETED = "COMPLETED"

    STATUS_CHOICES = [
        (DRAFT,     "Draft"),
        (ACTIVE,    "Active"),
        (CLOSED,    "Closed"),
        (COMPLETED, "Completed"),
    ]

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    ticket_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("500.00")
    )

    draw_date = models.DateField()

    max_ticket_number = models.PositiveIntegerField(
        default=60,
        help_text="Highest allowed ticket number (e.g. 60 means tickets 1–60)"
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=DRAFT
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
