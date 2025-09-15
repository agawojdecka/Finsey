import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.savings.models import Goal
from apps.users.models import User


@pytest.mark.django_db
def test_goal_progress(test_client: APIClient, test_user: User) -> None:
    goal = Goal.objects.create(
        title="Test",
        amount=1500,
        target_date="2025-12-31",
        user=test_user,
    )

    data = {"monthly_savings": 100, "goal_id": goal.id}

    response = test_client.post("/savings/goals/progress/", data)

    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    assert response_json == {"years_left": 1, "months_left": 3}
