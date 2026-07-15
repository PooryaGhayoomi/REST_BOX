from django.db import models
from reservations.models import Reservation


class Payment(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    gateway_ref = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Payment {self.id}"