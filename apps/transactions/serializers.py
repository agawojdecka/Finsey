from datetime import date
from decimal import Decimal
from typing import Any

from django.utils import timezone
from rest_framework import serializers

from apps.transactions.services.report import AVAILABLE_REPORT_FIELDS

from .models import Category, PlannedTransaction, Transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "account", "title", "transaction_type", "user"]
        read_only_fields = ["id", "user"]


class TransactionReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Transaction
        fields = [
            "id",
            "account",
            "title",
            "transaction_type",
            "amount",
            "category",
            "date",
            "description",
            "user",
        ]
        read_only_fields = ["id", "user"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "account",
            "title",
            "transaction_type",
            "amount",
            "category",
            "date",
            "description",
            "user",
            "created_at",
        ]
        read_only_fields = ["id", "user"]

    def validate_amount(self, value: Decimal) -> Decimal:
        """
        Ensure the amount is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def to_representation(self, instance: Transaction) -> Any:
        return TransactionReadSerializer(instance).data

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        account = attrs.get("account")
        category = attrs.get("category")

        if category and account and category.account != account:
            raise serializers.ValidationError(
                {"category": "The selected category does not belong to the specified account."}
            )

        return attrs


class ColumnsListSerializer(serializers.Serializer):
    selected_columns = serializers.ListField(child=serializers.ChoiceField(choices=AVAILABLE_REPORT_FIELDS))


class TransactionToSavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "amount",
        ]


class PlannedTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlannedTransaction
        fields = [
            "id",
            "account",
            "title",
            "amount",
            "category",
            "description",
            "is_monthly_payment",
            "user",
            "scheduled_at",
            "is_executed",
        ]
        read_only_fields = ["id", "user", "is_executed"]

        def validate_scheduled_at(self, value: date) -> date:
            if value <= timezone.now().date():
                raise serializers.ValidationError("Scheduled date must be after today.")
            return value
