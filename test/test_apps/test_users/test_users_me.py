import pytest
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

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
def test_get_user_info(test_client, test_user):
    response = test_client.get('/users/me/')
    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    assert response_json == {
        "id": test_user.id,
        "first_name": "",
        "last_name": "",
        "email": "",
        "username": "test",
        "phone_number": None,
        "date_of_birth": None
    }

    User.objects.get(id=response_json["id"])