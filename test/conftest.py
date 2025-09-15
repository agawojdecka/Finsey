from typing import cast

import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.users.models import User


@pytest.fixture
def test_user() -> User:
    user = User.objects.create_user(username='test', password='1234')
    return cast(User, user)


@pytest.fixture
def test_user2() -> User:
    user2 = User.objects.create_user(username='test2', password='1234')
    return cast(User, user2)


@pytest.fixture
def test_client(test_user: User) -> APIClient:
    token = Token.objects.create(user=test_user)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    return client
