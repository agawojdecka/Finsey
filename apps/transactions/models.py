from datetime import date

from django.db import models

from apps.accounts.models import Account
from apps.users.models import User


class Transaction(models.Model):
    class Types(models.TextChoices):
        INCOME = "INCOME"
        EXPENSE = "EXPENSE"

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, blank=False, related_name="transactions"
    )
    title = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=10, choices=Types)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, related_name="transactions"
    )
    date = models.DateField(default=date.today, blank=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    is_constant = models.BooleanField(default=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions"
    )

    def __str__(self):
        sign = "+" if self.transaction_type == self.Types.INCOME else "-"
        return f"{sign}{self.amount} {self.title}"


class Category(models.Model):
    class Types(models.TextChoices):
        INCOME = "INCOME"
        EXPENSE = "EXPENSE"

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, blank=False, related_name="categories"
    )
    title = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=10, choices=Types)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="categories")

    def __str__(self):
        return self.title
