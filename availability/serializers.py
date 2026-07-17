from rest_framework import serializers
from .models import Availability


class AvailabilitySerializer(serializers.ModelSerializer):
    """نمایش وضعیت یک روز مشخص از تقویم ویلا (فقط خواندنی)."""

    class Meta:
        model = Availability
        fields = ("id", "villa", "date", "is_available")
        read_only_fields = ("id", "villa")


class AvailabilityDaySerializer(serializers.Serializer):
    """یک آیتم ورودی برای بروزرسانی دستی یک روز توسط host."""

    date = serializers.DateField()
    is_available = serializers.BooleanField()


class AvailabilityBulkUpdateSerializer(serializers.Serializer):
    """
    بدنه‌ی درخواست PATCH برای باز/بسته کردن چند روز از تقویم به‌صورت یکجا:

    {
        "days": [
            {"date": "2025-07-01", "is_available": false},
            {"date": "2025-07-02", "is_available": false}
        ]
    }
    """

    days = AvailabilityDaySerializer(many=True)

    def validate_days(self, value):
        if not value:
            raise serializers.ValidationError("لیست days نباید خالی باشد.")
        return value
