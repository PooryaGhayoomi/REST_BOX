from django.urls import path
from .views import HelloAPIView, RegisterAPIView

urlpatterns = [
    path("", HelloAPIView.as_view()),
    path("auth/register/", RegisterAPIView.as_view()),
]