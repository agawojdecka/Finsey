from datetime import date

from django.db import models

from apps.users.models import User


class Document(models.Model):
    class Types(models.TextChoices):
        PDF = "PDF", "PDF"

    name = models.CharField(max_length=255, blank=False)
    title = models.CharField(max_length=255, blank=True)
    document_type = models.CharField(max_length=10, choices=Types)
    uploaded_at = models.DateField(default=date.today, blank=True, db_index=True)
    note = models.TextField(blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="documents"
    )

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}.{self.document_type}"