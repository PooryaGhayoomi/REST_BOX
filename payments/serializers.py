from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = (
            "status",
            "gateway_ref",
            "created_at",
        )


class PaymentVerifySerializer(serializers.Serializer):

    reservation_id = serializers.IntegerField()