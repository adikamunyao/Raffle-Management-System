from django.contrib.auth.models import AbstractUser
from django.db import models

DEFAULT_PASSWORD = "YouthDay@2026"


class User(AbstractUser):

    SECRETARY = "SECRETARY"
    TREASURER = "TREASURER"
    ADMIN = "ADMIN"

    ROLE_CHOICES = [
        (SECRETARY, "Secretary"),
        (TREASURER, "Treasurer"),
        (ADMIN, "Admin"),
    ]

    ROLE_DESCRIPTIONS = {
        SECRETARY: "Submits M-Pesa SMS messages and generates tickets for members.",
        TREASURER: "Views payment records and financial summaries.",
        ADMIN: "Manages events, prizes, draws and all staff accounts.",
    }

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=SECRETARY,
        db_index=True,
    )

    must_change_password = models.BooleanField(
        default=True,
        help_text="Force password change on next login."
    )

    def is_secretary(self):
        return self.role == self.SECRETARY

    def is_treasurer(self):
        return self.role == self.TREASURER

    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return self.get_full_name() or self.username