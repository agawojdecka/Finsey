import pytest
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.transactions.models import Category
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
def test_create_category(test_client, test_user):
    data = {
        "title": "test category",
        "transaction_type": "EXPENSE",
    }
    response = test_client.post("/transactions/categories/", data)

    assert response.status_code == status.HTTP_201_CREATED

    response_json = response.json()
    assert response_json == {
        "id": 1,
        "title": "test category",
        "transaction_type": "EXPENSE",
        "user": test_user.id
    }

    Category.objects.get(id=response_json["id"])


@pytest.mark.django_db
def test_get_categories_list(test_client, test_user, test_user2):
    category_1 = Category.objects.create(title="test 1", transaction_type="EXPENSE", user=test_user)
    Category.objects.create(title="test 2", transaction_type="INCOME", user=test_user2)

    response = test_client.get("/transactions/categories/")

    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    assert response_json == [{
        "id": category_1.id,
        "title": "test 1",
        "transaction_type": "EXPENSE",
        "user": test_user.id
    }]
