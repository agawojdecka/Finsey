import pytest

from apps.savings.models import Goal, Saving
from apps.savings.services.total_saved import calculate_total_saved
from apps.users.models import User


@pytest.mark.django_db
def test_calculate_total_saved():
    user = User.objects.create_user(username='test', password='1234')
    goal = Goal.objects.create(title="Test Goal", amount=2000, user=user)
    Saving.objects.create(operation_type="INFLOW", user=user, amount=200, goal=goal)
    Saving.objects.create(operation_type="OUTFLOW", user=user, amount=100, goal=goal)

    total_saved = calculate_total_saved(goal)

    assert total_saved == 100
