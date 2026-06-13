# Create your models here.
from django.db import models


class Member(models.Model):

    name = models.CharField(
        max_length=255,
        db_index=True
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