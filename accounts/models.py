# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    SECRETARY = "SECRETARY"
    TREASURER = "TREASURER"
    ADMIN = "ADMIN"

    ROLE_CHOICES = [
        (SECRETARY, "Secretary"),
        (TREASURER, "Treasurer"),
        (ADMIN, "Admin"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=SECRETARY,
        db_index=True,
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