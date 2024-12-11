from rest_framework import serializers

from .models import Transaction, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "transaction_type", "user"]
        read_only_fields = ["id", "user"]


class TransactionReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Transaction
        fields = [
            "id",  # Including `id` to identify transactions
            "title",
            "transaction_type",
            "amount",
            "category",
            "date",
            "description",
            "is_constant",
            "user",
        ]
        read_only_fields = ["id"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",  # Including `id` to identify transactions
            "title",
            "transaction_type",
            "amount",
            "category",
            "date",
            "description",
            "is_constant",
        ]
        read_only_fields = ["id", "user"]

    def validate_amount(self, value):
        """
        Ensure the amount is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate_type(self, data):
        """
        Additional validation to ensure logical constraints between fields.
        """
        if data["transaction_type"] not in [
            Transaction.Types.INCOME,
            Transaction.Types.EXPENSE,
        ]:
            raise serializers.ValidationError("Invalid transaction type.")
        return data

    def to_representation(self, instance):
        return TransactionReadSerializer(instance).data
