from django.urls import path

from .views import (
    VillaListCreateAPIView,
    VillaDetailAPIView,
)

urlpatterns = [

    path(
        "",
        VillaListCreateAPIView.as_view(),
        name="villa-list-create",
    ),

    path(
        "<int:pk>/",
        VillaDetailAPIView.as_view(),
        name="villa-detail",
    ),

]