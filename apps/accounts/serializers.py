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
            "user",
        ]
        read_only_fields = ["id", "user", "account_number"]
