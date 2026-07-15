from django.urls import path
from .views import ReservationCreateAPIView

urlpatterns = [
    path(
        "",
        ReservationCreateAPIView.as_view(),
        name="reservation-create",
    ),
]