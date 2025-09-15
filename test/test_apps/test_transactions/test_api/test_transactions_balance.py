import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.transactions.models import Transaction
from apps.users.models import User


@pytest.mark.django_db
def test_get_balance(test_client: APIClient, test_user: User) -> None:
    Transaction.objects.create(
        title="test income",
        transaction_type="INCOME",
        amount=1000,
        user=test_user,
    )
    Transaction.objects.create(
        title="test expense",
        transaction_type="EXPENSE",
        amount=200,
        user=test_user,
    )

    response = test_client.get("/transactions/balance/")

    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    assert response_json == {"income": 1000.0, "expense": 200.0, "balance": 800.0}
