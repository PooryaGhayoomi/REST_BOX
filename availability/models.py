from django.db import models
from villas.models import Villa


class Availability(models.Model):

    villa = models.ForeignKey(
        Villa,
        on_delete=models.CASCADE,
        related_name="availabilities"
    )

    date = models.DateField()

    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ("villa", "date")
        ordering = ["date"]

    def __str__(self):
        state = "Free" if self.is_available else "Booked"
        return f"{self.villa.title} - {self.date} - {state}"
