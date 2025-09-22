from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    inactivity_notification_sent_at = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.username}"
