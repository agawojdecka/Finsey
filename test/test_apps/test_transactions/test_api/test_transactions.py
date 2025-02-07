import pytest
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.transactions.models import Transaction
from apps.users.models import User


@pytest.fixture
def test_user():
    user = User.objects.create_user(username='test', password='1234')
    return user


@pytest.fixture
def test_user2():
    user2 = User.objects.create_user(username='test2', password='1234')
    return user2


@pytest.fixture
def test_client(test_user):
    token = Token.objects.create(user=test_user)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    return client


@pytest.mark.django_db
def test_create_transaction(test_client, test_user):
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
        "category": None,
        "date": timezone.now().date().isoformat(),
        "description": None,
        "is_constant": False,
        "user": test_user.id
    }

    Transaction.objects.get(id=response_json["id"])


@pytest.mark.django_db
def test_get_transactions_list(test_client, test_user, test_user2):
    transaction_1 = Transaction.objects.create(title="test 1", transaction_type="INCOME", amount=100, user=test_user)
    Transaction.objects.create(title="test 2", transaction_type="EXPENSE", amount=100, user=test_user2)

    response = test_client.get("/transactions/")

    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    assert response_json == [{
        "id": transaction_1.id,
        "title": "test 1",
        "transaction_type": "INCOME",
        "amount": "100.00",
        "category": None,
        "date": timezone.now().date().isoformat(),
        "description": None,
        "is_constant": False,
        "user": test_user.id
    }]
