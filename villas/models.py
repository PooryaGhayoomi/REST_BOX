from django.db import models
from users.models import User


class Villa(models.Model):

    host = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="villas"
    )

    title = models.CharField(max_length=150)

    city = models.CharField(max_length=100)

    address = models.TextField()

    description = models.TextField()

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title