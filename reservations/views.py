from datetime import datetime

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from villas.models import Villa
from .models import Reservation
from .serializers import ReservationSerializer


class ReservationCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ReservationSerializer(data=request.data)

        if serializer.is_valid():

            villa = Villa.objects.get(id=request.data["villa"])

            check_in = datetime.strptime(
                request.data["check_in"],
                "%Y-%m-%d"
            ).date()

            check_out = datetime.strptime(
                request.data["check_out"],
                "%Y-%m-%d"
            ).date()

            nights = (check_out - check_in).days

            total_price = villa.price_per_night * nights

            reservation = serializer.save(
                guest=request.user,
                total_price=total_price,
                status="pending_payment"
            )

            return Response(
                ReservationSerializer(reservation).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )