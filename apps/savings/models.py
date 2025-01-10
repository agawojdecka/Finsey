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
    goal = models.ForeignKey("Goal", on_delete=models.SET_NULL, null=True,
                             related_name="savings")  # Emergency Fund, Vacation, Car etc.
    date = models.DateField(default=date.today, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        sign = "+" if self.operation_type == self.Types.INFLOW else "-"
        return f"{sign}{self.amount} {self.goal}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.goal:
            self.goal.update_completion_status()

class Goal(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    target_date = models.DateField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goals")
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.amount} {self.title}"

    def update_completion_status(self):
        total_saved = sum(
            saving.amount for saving in self.savings.filter(operation_type=Saving.Types.INFLOW)
        ) - sum(
            saving.amount for saving in self.savings.filter(operation_type=Saving.Types.OUTFLOW)
        )
        self.is_completed = total_saved >= self.amount
        self.save()
