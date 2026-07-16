from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Villa
from .serializers import VillaSerializer
from .permissions import IsHost
from rest_framework.generics import ListAPIView, RetrieveAPIView

from rest_framework.generics import ListCreateAPIView

from django.db.models import Count, Q
from django.utils.dateparse import parse_date

class VillaListCreateAPIView(ListCreateAPIView):

    serializer_class = VillaSerializer

    def get_queryset(self):
        queryset = Villa.objects.all()

        city = self.request.query_params.get("city")

        if city:
            queryset = queryset.filter(city__iexact=city)

        check_in = self.request.query_params.get("check_in")
        check_out = self.request.query_params.get("check_out")
        if check_in and check_out:
            check_in_date = parse_date(check_in)
            check_out_date = parse_date(check_out)
            if check_in_date and check_out_date and check_in_date < check_out_date:
                nights_requested = (check_out_date - check_in_date).days

                queryset = queryset.annotate(
                    free_nights=Count(
                        "availabilities",
                        filter=Q(
                            availabilities__date__gte=check_in_date,
                            availabilities__date__lt=check_out_date,
                            availabilities__is_available=True,
                        ),
                    )
                ).filter(free_nights=nights_requested)
        return queryset

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsHost()]
        return []

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

class VillaDetailAPIView(RetrieveAPIView):

    queryset = Villa.objects.all()
    serializer_class = VillaSerializer