import pytest
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
def test_client(test_user):
    token = Token.objects.create(user=test_user)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    return client


@pytest.mark.django_db
def test_get_balance(test_client, test_user):
    Transaction.objects.create(title="test income", transaction_type="INCOME", amount=1000, user=test_user)
    Transaction.objects.create(title="test expense", transaction_type="EXPENSE", amount=200, user=test_user)

    response = test_client.get("/transactions/balance/")

    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    assert response_json == {
        "incomes": 1000.0,
        "expenses": 200.0,
        "balance": 800.0
    }
