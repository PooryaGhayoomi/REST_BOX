from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from villas.models import Villa
from .models import Availability

CALENDAR_HORIZON_DAYS = 180


@receiver(post_save, sender=Villa)
def create_villa_calendar(sender, instance, created, **kwargs):

    if not created:
        return

    today = timezone.localdate()

    Availability.objects.bulk_create([
        Availability(
            villa=instance,
            date=today + timedelta(days=day_offset),
            is_available=True,
        )
        for day_offset in range(CALENDAR_HORIZON_DAYS)
    ])
