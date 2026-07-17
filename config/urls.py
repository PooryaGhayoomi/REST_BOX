from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Users
    path("api/", include("users.urls")),

    # Authentication
    path(
        "api/auth/login/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "api/auth/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    # Villas
    path(
        "api/villas/",
        include("villas.urls"),
    ),

    # Availability
    path(
        "api/availability/",
        include("availability.urls"),
    ),

    # Reservations
    path(
        "api/reservations/",
        include("reservations.urls"),
    ),
    
    path(
    "api/payments/",
    include("payments.urls"),
),
]