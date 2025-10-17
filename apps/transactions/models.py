from datetime import date
from typing import cast

from django.db import models

from apps.accounts.models import Account
from apps.users.models import User


class TransactionBase(models.Model):
    class Types(models.TextChoices):
        INCOME = "INCOME"
        EXPENSE = "EXPENSE"

    account = models.ForeignKey(  # TODO Make account not nullable
        Account,
        on_delete=models.CASCADE,
        null=True,
        blank=False,
        related_name="%(class)ss",  # dynamic related_name
    )
    title = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=10, choices=Types)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)ss",
    )
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)ss",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Transaction(TransactionBase):
    date = models.DateField(default=date.today, blank=True, db_index=True)

    def __str__(self) -> str:
        sign = "+" if self.transaction_type == self.Types.INCOME else "-"
        return f"{sign}{self.amount} {self.title}"


class PlannedTransaction(TransactionBase):
    transaction_type = "EXPENSE"
    scheduled_at = models.DateField(db_index=True)
    is_monthly_payment = models.BooleanField(default=False)
    is_executed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Transaction scheduled at {self.scheduled_at}: {self.amount} {self.title}"


class Category(models.Model):
    class Types(models.TextChoices):
        INCOME = "INCOME"
        EXPENSE = "EXPENSE"

    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=False, related_name="categories")
    title = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=10, choices=Types)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="categories")

    def __str__(self) -> str:
        return cast(str, self.title)
