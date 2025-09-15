import pytest
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from apps.transactions.models import Transaction
from apps.users.models import User


@pytest.mark.django_db
def test_create_transaction(test_client: APIClient, test_user: User) -> None:
    data = {
        "title": "test",
        "transaction_type": "INCOME",
        "amount": 100,
    }
    response = test_client.post("/transactions/", data)

    assert response.status_code == status.HTTP_201_CREATED

    response_json = response.json()
    assert response_json == {
        "id": 1,
        "title": "test",
        "transaction_type": "INCOME",
        "amount": "100.00",
        "account": None,
        "category": None,
        "date": timezone.now().date().isoformat(),
        "description": None,
        "is_constant": False,
        "user": test_user.id,
    }

    Transaction.objects.get(id=response_json["id"])


@pytest.mark.django_db
def test_get_transactions_list(test_client: APIClient, test_user: User, test_user2: User) -> None:
    transaction_1 = Transaction.objects.create(title="test 1", transaction_type="INCOME", amount=100, user=test_user)
    Transaction.objects.create(title="test 2", transaction_type="EXPENSE", amount=100, user=test_user2)

    response = test_client.get("/transactions/")

    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    assert response_json == [
        {
            "id": transaction_1.id,
            "title": "test 1",
            "transaction_type": "INCOME",
            "amount": "100.00",
            "account": None,
            "category": None,
            "date": timezone.now().date().isoformat(),
            "description": None,
            "is_constant": False,
            "user": test_user.id,
        }
    ]
