import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.savings.models import Goal
from apps.users.models import User


@pytest.mark.django_db
def test_create_goal(test_client: APIClient, test_user: User) -> None:
    data = {"title": "Test Goal", "target_date": "2025-12-31", "amount": 10000}

    response = test_client.post("/savings/goals/", data)

    assert response.status_code == status.HTTP_201_CREATED

    response_json = response.json()
    assert response_json == {
        "id": 1,
        "title": "Test Goal",
        "target_date": "2025-12-31",
        "amount": "10000.00",
        "user": test_user.id,
        "description": None,
        "is_completed": False,
        "notification_sent": False,
    }

    Goal.objects.get(id=response_json["id"])


@pytest.mark.django_db
def test_get_goals_list(test_client: APIClient) -> None:
    response = test_client.get("/savings/goals/")

    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    assert response_json == []
