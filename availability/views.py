from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from villas.models import Villa

from .models import Availability
from .permissions import IsVillaOwnerHost
from .serializers import AvailabilityBulkUpdateSerializer, AvailabilitySerializer
from django.db import transaction
from availability.models import Availability

class VillaAvailabilityListAPIView(ListAPIView):

    serializer_class = AvailabilitySerializer

    def get_queryset(self):
        villa_id = self.kwargs["villa_id"]
        get_object_or_404(Villa, pk=villa_id)

        queryset = Availability.objects.filter(villa_id=villa_id)

        only_free = self.request.query_params.get("only_free")
        if only_free in ("true", "1"):
            queryset = queryset.filter(is_available=True)

        return queryset


class VillaAvailabilityUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsVillaOwnerHost]

    def patch(self, request, villa_id):
        villa = get_object_or_404(Villa, pk=villa_id)

        if villa.host_id != request.user.id:
            return Response(
                {"detail": "شما مالک این ویلا نیستید."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = AvailabilityBulkUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_rows = []
        for day in serializer.validated_data["days"]:
            availability, _ = Availability.objects.update_or_create(
                villa=villa,
                date=day["date"],
                defaults={"is_available": day["is_available"]},
            )
            updated_rows.append(availability)

        return Response(
            AvailabilitySerializer(updated_rows, many=True).data,
            status=status.HTTP_200_OK,
        )
