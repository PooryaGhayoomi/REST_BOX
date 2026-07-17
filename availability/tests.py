from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from villas.models import Villa

from .models import Availability
from .signals import CALENDAR_HORIZON_DAYS


class AvailabilityAutoGenerationTests(APITestCase):

    def setUp(self):
        self.host = User.objects.create_user(
            username="host1",
            password="StrongPass123",
            role="HOST",
        )

    def test_calendar_created_on_villa_save(self):
        villa = Villa.objects.create(
            host=self.host,
            title="ویلای تست",
            city="تهران",
            address="خیابان تست",
            description="توضیحات",
            price_per_night=1000000,
        )

        self.assertEqual(
            Availability.objects.filter(villa=villa).count(),
            CALENDAR_HORIZON_DAYS,
        )
        self.assertTrue(
            Availability.objects.filter(villa=villa, is_available=True).exists()
        )


class VillaAvailabilityAPITests(APITestCase):
    def setUp(self):
        self.host = User.objects.create_user(
            username="host2",
            password="StrongPass123",
            role="HOST",
        )
        self.other_host = User.objects.create_user(
            username="host3",
            password="StrongPass123",
            role="HOST",
        )
        self.guest = User.objects.create_user(
            username="guest1",
            password="StrongPass123",
            role="GUEST",
        )
        self.villa = Villa.objects.create(
            host=self.host,
            title="ویلای شمال",
            city="رشت",
            address="جاده جنگلی",
            description="توضیحات",
            price_per_night=2000000,
        )

    def test_anyone_can_view_villa_calendar(self):
        url = f"/api/villas/{self.villa.id}/availability/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), CALENDAR_HORIZON_DAYS)

    def test_owner_host_can_close_days(self):
        self.client.force_authenticate(user=self.host)

        today = timezone.localdate()
        url = f"/api/villas/{self.villa.id}/availability/update/"
        payload = {
            "days": [
                {"date": str(today), "is_available": False},
                {"date": str(today + timedelta(days=1)), "is_available": False},
            ]
        }

        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Availability.objects.filter(villa=self.villa, is_available=False).count(),
            2,
        )

    def test_other_host_cannot_update_calendar(self):
        self.client.force_authenticate(user=self.other_host)

        today = timezone.localdate()
        url = f"/api/villas/{self.villa.id}/availability/update/"
        payload = {"days": [{"date": str(today), "is_available": False}]}

        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_guest_cannot_update_calendar(self):
        self.client.force_authenticate(user=self.guest)

        today = timezone.localdate()
        url = f"/api/villas/{self.villa.id}/availability/update/"
        payload = {"days": [{"date": str(today), "is_available": False}]}

        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class VillaSearchByDateRangeTests(APITestCase): 

    def setUp(self):
        self.host = User.objects.create_user(
            username="host4",
            password="StrongPass123",
            role="HOST",
        )
        self.villa_free = Villa.objects.create(
            host=self.host,
            title="ویلای خالی",
            city="کیش",
            address="آدرس ۱",
            description="توضیحات",
            price_per_night=1500000,
        )
        self.villa_booked = Villa.objects.create(
            host=self.host,
            title="ویلای رزرو شده",
            city="کیش",
            address="آدرس ۲",
            description="توضیحات",
            price_per_night=1500000,
        )

        today = timezone.localdate()
        Availability.objects.filter(
            villa=self.villa_booked,
            date=today + timedelta(days=1),
        ).update(is_available=False)

    def test_search_excludes_villa_with_booked_day_in_range(self):
        today = timezone.localdate()
        check_in = today
        check_out = today + timedelta(days=3)

        url = f"/api/villas/?city=کیش&check_in={check_in}&check_out={check_out}"
        response = self.client.get(url)

        returned_titles = [item["title"] for item in response.data]

        self.assertIn("ویلای خالی", returned_titles)
        self.assertNotIn("ویلای رزرو شده", returned_titles)
