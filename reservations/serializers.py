from rest_framework import serializers
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = "__all__"
        read_only_fields = (
            "guest",
            "total_price",
            "status",
            "created_at",
        )