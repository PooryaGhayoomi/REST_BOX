from datetime import datetime

from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from availability.models import Availability
from villas.models import Villa

from .models import Reservation
from .serializers import ReservationSerializer


class ReservationCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ReservationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        villa = get_object_or_404(
            Villa,
            id=request.data["villa"],
        )

        check_in = datetime.strptime(
            request.data["check_in"],
            "%Y-%m-%d",
        ).date()

        check_out = datetime.strptime(
            request.data["check_out"],
            "%Y-%m-%d",
        ).date()

        if check_in >= check_out:
            return Response(
                {"error": "Check-out date must be after check-in date."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        nights = (check_out - check_in).days

        with transaction.atomic():

            available_days = (
                Availability.objects
                .select_for_update()
                .filter(
                    villa=villa,
                    date__gte=check_in,
                    date__lt=check_out,
                    is_available=True,
                )
            )

            if available_days.count() != nights:
                return Response(
                    {"error": "Selected dates are not available."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            total_price = villa.price_per_night * nights

            reservation = serializer.save(
                guest=request.user,
                total_price=total_price,
                status="pending_payment",
            )

            available_days.update(is_available=False)

        return Response(
            ReservationSerializer(reservation).data,
            status=status.HTTP_201_CREATED,
        )


class ReservationListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        reservations = Reservation.objects.filter(
            guest=request.user
        ).order_by("-created_at")

        serializer = ReservationSerializer(
            reservations,
            many=True,
        )

        return Response(serializer.data)