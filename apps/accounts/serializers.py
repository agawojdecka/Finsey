from rest_framework import serializers

from apps.accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "account_number",
            "account_type",
            "name",
            "description",
            "currency",
            "user",
        ]
        read_only_fields = ["id", "account_number", "account_type", "currency", "user"]