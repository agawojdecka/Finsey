import pytest
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.savings.models import Saving
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
def test_create_saving(test_client, test_user):
    data = {
        "operation_type": "INFLOW",
        "amount": 100,
    }
    response = test_client.post("/savings/", data)

    assert response.status_code == status.HTTP_201_CREATED

    response_json = response.json()
    assert response_json == {
        "id": 1,
        "operation_type": "INFLOW",
        "amount": "100.00",
        "user": test_user.id,
        "goal": None,
        "date": timezone.now().date().isoformat(),
        "description": None,
    }

    Saving.objects.get(id=response_json["id"])


@pytest.mark.django_db
def test_get_savings_list(test_client):
    response = test_client.get("/savings/")

    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    assert response_json == []
