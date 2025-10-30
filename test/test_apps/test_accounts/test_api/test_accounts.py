import uuid
from unittest.mock import patch

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import Account
from apps.users.models import User


@pytest.mark.django_db
def test_create_account(test_client: APIClient, test_user: User) -> None:
    fake_uuid = str(uuid.UUID("12345678-1234-5678-1234-567812345678"))

    with patch("apps.core.utils.identifiers.uuid.uuid4", return_value=fake_uuid) as mock_uuid:

        data = {
            "account_type": "MAIN",
            "name": "Test",
            "user": test_user.id,
        }
        response = test_client.post("/accounts/", data)

        assert response.status_code == status.HTTP_201_CREATED

        response_json = response.json()
        mock_uuid.assert_called_once()
        assert response_json == {
            "account_number": fake_uuid,
            "id": 1,
            "account_type": "MAIN",
            "name": "Test",
            "description": None,
            "user": 1,
        }

        Account.objects.get(id=response_json["id"])


@pytest.mark.django_db
def test_get_accounts_list(test_client: APIClient, test_user: User, test_user2: User) -> None:
    fake_uuid = str(uuid.UUID("12345678-1234-5678-1234-567812345678"))
    Account.objects.create(account_type="MAIN", name="Test 2", user=test_user2)

    with patch("apps.core.utils.identifiers.uuid.uuid4", return_value=fake_uuid) as mock_uuid:
        account_1 = Account.objects.create(account_type="MAIN", name="Test 1", user=test_user)

        response = test_client.get("/accounts/")

        assert response.status_code == status.HTTP_200_OK

        mock_uuid.assert_called_once()

        response_json = response.json()
        assert response_json == [
            {
                "account_number": fake_uuid,
                "account_type": "MAIN",
                "description": None,
                "id": account_1.id,
                "name": "Test 1",
                "user": test_user.id,
            }
        ]


@pytest.mark.django_db
def test_get_account_detail(test_client: APIClient, test_user: User) -> None:
    fake_uuid = str(uuid.UUID("12345678-1234-5678-1234-567812345678"))

    with patch("apps.core.utils.identifiers.uuid.uuid4", return_value=fake_uuid):

        account = Account.objects.create(account_type="MAIN", name="Test", user=test_user, account_number=fake_uuid)

        response = test_client.get("/accounts/1/")

        assert response.status_code == status.HTTP_200_OK

        response_json = response.json()

        assert response_json == {
            "account_number": fake_uuid,
            "id": account.id,
            "account_type": "MAIN",
            "name": "Test",
            "description": None,
            "user": test_user.id,
        }
