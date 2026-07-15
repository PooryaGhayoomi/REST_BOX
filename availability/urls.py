from django.urls import path

from .views import (
    VillaAvailabilityListAPIView,
    VillaAvailabilityUpdateAPIView,
)

urlpatterns = [

    path(
        "<int:villa_id>/availability/",
        VillaAvailabilityListAPIView.as_view(),
        name="villa-availability-list",
    ),

    path(
        "<int:villa_id>/availability/update/",
        VillaAvailabilityUpdateAPIView.as_view(),
        name="villa-availability-update",
    ),

]
