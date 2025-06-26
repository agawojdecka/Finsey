from rest_framework import serializers

from apps.transactions.services.report import AVAILABLE_REPORT_FIELDS
from .models import Transaction, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "account",
            "title",
            "transaction_type",
            "user"
        ]
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
            "is_constant",
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
            "is_constant",
            "user",
        ]
        read_only_fields = ["id", "user"]

    def validate_amount(self, value):
        """
        Ensure the amount is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def to_representation(self, instance):
        return TransactionReadSerializer(instance).data

    def validate(self, attrs):
        account = attrs.get("account")
        category = attrs.get("category")

        if category and account and category.account != account:
            raise serializers.ValidationError({
                "category": "The selected category does not belong to the specified account."
            })

        return attrs


class ColumnsListSerializer(serializers.Serializer):
    selected_columns = serializers.ListField(child=serializers.ChoiceField(choices=AVAILABLE_REPORT_FIELDS))


class TransactionToSavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "amount",
        ]