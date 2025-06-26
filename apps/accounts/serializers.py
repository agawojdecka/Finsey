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
        read_only_fields = ["id", "user"]

    def get_fields(self):
        fields = super().get_fields()
        if self.instance:
            fields['account_number'].read_only = True
        return fields