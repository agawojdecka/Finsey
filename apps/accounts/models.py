from django.db import models

from apps.users.models import User


class Account(models.Model):
    class Types(models.TextChoices):
        MAIN = "MAIN"
        SAVINGS = "SAVINGS"
        SUPPORT = "SUPPORT"
        INVESTMENT = "INVESTMENT"
        CREDIT = "CREDIT"
        BUSINESS = "BUSINESS"

    class Currencies(models.TextChoices):
        PLN = "PLN"
        USD = "USD"
        EUR = "EUR"
        GBP = "GBP"

    account_number = models.CharField(max_length=32, unique=True)
    account_type = models.CharField(max_length=10, choices=Types)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    currency = models.CharField(max_length=3, choices=Currencies)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="accounts"
    )

    def __str__(self):
        return f"{self.name} ({self.get_account_type_display()}) - **** {self.account_number[-4:]}"