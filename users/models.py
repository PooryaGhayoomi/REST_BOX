from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    class Role(models.TextChoices):
        HOST = "HOST", "Host"
        GUEST = "GUEST", "Guest"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.GUEST,
    )