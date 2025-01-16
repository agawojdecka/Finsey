import pytest

from apps.savings.models import Goal, Saving
from apps.savings.services.goal_progess import calculate_goal_progress
from apps.users.models import User


@pytest.mark.django_db
def test_calculate_goal_progress():
    user = User.objects.create_user(username='test', password='1234')
    goal = Goal.objects.create(title="Test Goal", amount=2000, user=user)
    Saving.objects.create(operation_type="INFLOW", user=user, amount=200, goal=goal)
    Saving.objects.create(operation_type="OUTFLOW", user=user, amount=100, goal=goal)
    monthly_savings = 100

    goal_progress = calculate_goal_progress(goal, monthly_savings)

    expected_results = {
        "years_left": 1,
        "months_left": 7
    }

    assert goal_progress == expected_results
