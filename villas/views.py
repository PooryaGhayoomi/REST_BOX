from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Villa
from .serializers import VillaSerializer
from .permissions import IsHost


class CreateVillaAPIView(CreateAPIView):

    queryset = Villa.objects.all()
    serializer_class = VillaSerializer

    permission_classes = [
        IsAuthenticated,
        IsHost,
    ]

    def perform_create(self, serializer):

        serializer.save(host=self.request.user)