from django.urls import path

from .views import (
    ReservationCreateAPIView,
    ReservationListAPIView,
)

urlpatterns = [
    path(
        "",
        ReservationCreateAPIView.as_view(),
        name="reservation-create",
    ),

    path(
        "history/",
        ReservationListAPIView.as_view(),
        name="reservation-history",
    ),
]