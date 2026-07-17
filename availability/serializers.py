from rest_framework import serializers
from .models import Availability


class AvailabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Availability
        fields = ("id", "villa", "date", "is_available")
        read_only_fields = ("id", "villa")


class AvailabilityDaySerializer(serializers.Serializer):

    date = serializers.DateField()
    is_available = serializers.BooleanField()


class AvailabilityBulkUpdateSerializer(serializers.Serializer):

    days = AvailabilityDaySerializer(many=True)

    def validate_days(self, value):
        if not value:
            raise serializers.ValidationError("لیست days نباید خالی باشد.")
        return value
