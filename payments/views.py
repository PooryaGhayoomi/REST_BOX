import random

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from reservations.models import Reservation

from .models import Payment
from .serializers import PaymentVerifySerializer


class PaymentVerifyAPIView(APIView):

    def post(self, request):

        serializer = PaymentVerifySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        reservation = get_object_or_404(
            Reservation,
            id=serializer.validated_data["reservation_id"],
        )

        payment = Payment.objects.create(
            reservation=reservation,
            amount=reservation.total_price,
            status="success",
            gateway_ref=str(random.randint(100000, 999999)),
        )

        reservation.status = "confirmed"
        reservation.save()

        return Response(
            {
                "message": "Payment successful.",
                "payment_id": payment.id,
                "gateway_ref": payment.gateway_ref,
            },
            status=status.HTTP_200_OK,
        )