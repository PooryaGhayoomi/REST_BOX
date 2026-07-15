from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from villas.models import Villa
from .models import Availability

# طبق سناریوی پروژه: وقتی host یک ویلای جدید ثبت می‌کند،
# تقویم آن باید برای ۶ ماه آینده (۱۸۰ روز) به صورت پیش‌فرض «خالی» باز شود.
CALENDAR_HORIZON_DAYS = 180


@receiver(post_save, sender=Villa)
def create_villa_calendar(sender, instance, created, **kwargs):
    """
    هر بار که یک Villa جدید ساخته می‌شود، ۱۸۰ روز آینده را
    به صورت is_available=True در تقویم آن ویلا ایجاد می‌کند.
    """
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
