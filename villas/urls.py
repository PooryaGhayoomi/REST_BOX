from django.urls import path
from .views import CreateVillaAPIView

urlpatterns = [
    path(
        "",
        CreateVillaAPIView.as_view(),
        name="create-villa",
    ),
]