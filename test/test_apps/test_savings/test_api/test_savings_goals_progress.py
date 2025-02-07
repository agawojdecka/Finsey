import pytest
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.savings.models import Goal
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
def test_goal_progress(test_client, test_user):
    goal = Goal.objects.create(title="Test", amount=1500, target_date="2025-12-31", user=test_user)

    data = {
        "monthly_savings": 100,
        "goal_id": goal.id
    }

    response = test_client.post("/savings/goals/progress/", data)

    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    assert response_json == {
        "years_left": 1,
        "months_left": 3
    }
