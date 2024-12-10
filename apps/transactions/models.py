from django.db import models
from django.utils import timezone


class Transaction(models.Model):
    class Types(models.TextChoices):
        INCOME = "INCOME"
        EXPENSE = "EXPENSE"

    title = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=10, choices=Types)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name="transactions")
    date = models.DateField(default=timezone.now().date(), blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.transaction_type} ({self.amount})"


class Category(models.Model):
    class Types(models.TextChoices):
        INCOME = "INCOME"
        EXPENSE = "EXPENSE"

    title = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=10, choices=Types)

    def __str__(self):
        return self.title
