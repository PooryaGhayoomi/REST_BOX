from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Villa
from .serializers import VillaSerializer
from .permissions import IsHost
from rest_framework.generics import ListAPIView, RetrieveAPIView

from rest_framework.generics import ListCreateAPIView

class VillaListCreateAPIView(ListCreateAPIView):

    serializer_class = VillaSerializer

    def get_queryset(self):
        queryset = Villa.objects.all()

        city = self.request.query_params.get("city")

        if city:
            queryset = queryset.filter(city__iexact=city)

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