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


class VillaAvailabilityListAPIView(ListAPIView):
    """
    GET /api/villas/{villa_id}/availability/

    نمایش تقویم یک ویلا (روزهای خالی و پر). این endpoint عمومی است
    تا guest بتواند قبل از رزرو، روزهای خالی ویلا را ببیند.

    پارامتر اختیاری ?only_free=true فقط روزهای خالی را برمی‌گرداند.
    """

    serializer_class = AvailabilitySerializer

    def get_queryset(self):
        villa_id = self.kwargs["villa_id"]
        # اگر ویلا وجود نداشته باشد، خطای 404 برگردانده شود
        get_object_or_404(Villa, pk=villa_id)

        queryset = Availability.objects.filter(villa_id=villa_id)

        only_free = self.request.query_params.get("only_free")
        if only_free in ("true", "1"):
            queryset = queryset.filter(is_available=True)

        return queryset


class VillaAvailabilityUpdateAPIView(APIView):
    """
    PATCH /api/villas/{villa_id}/availability/update/

    فقط hostِ مالکِ ویلا می‌تواند روزهای مشخصی از تقویم را
    باز یا بسته کند (مثلاً برای مسدود کردن دستی چند روز).

    بدنه‌ی درخواست:
    {
        "days": [
            {"date": "2025-07-01", "is_available": false},
            {"date": "2025-07-02", "is_available": true}
        ]
    }
    """

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
