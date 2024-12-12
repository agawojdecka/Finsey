from datetime import date

from django.db import models

from apps.users.models import User


class Saving(models.Model):
    class Types(models.TextChoices):
        INFLOW = "INFLOW"
        OUTFLOW = "OUTFLOW"

    operation_type = models.CharField(max_length=10, choices=Types)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="savings")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.ForeignKey("Purpose", on_delete=models.SET_NULL, null=True, related_name="savings")  # Emergency Fund, Vacation, Car etc.
    date = models.DateField(default=date.today, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        sign = "+" if self.operation_type == "INFLOW" else "-"
        return f"{sign}{self.amount} {self.purpose}"


class Purpose(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purposes")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
