from django.db import models

from apps.core.utils.identifiers import str_uuid
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

    account_number = models.CharField(max_length=36, unique=True, default=str_uuid)
    account_type = models.CharField(max_length=10, choices=Types)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    currency = models.CharField(max_length=3, choices=Currencies)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="accounts",
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.get_account_type_display()}) " f"- **** {self.account_number[-4:]}"
