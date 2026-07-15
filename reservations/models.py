from django.db import models
from users.models import User
from villas.models import Villa


class Reservation(models.Model):

    STATUS_CHOICES = [
        ("pending_payment", "Pending Payment"),
        ("confirmed", "Confirmed"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]

    guest = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    villa = models.ForeignKey(
        Villa,
        on_delete=models.CASCADE
    )

    check_in = models.DateField()

    check_out = models.DateField()

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending_payment"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.guest.username} - {self.villa.title}"