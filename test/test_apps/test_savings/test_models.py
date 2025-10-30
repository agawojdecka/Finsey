import pytest

from apps.savings.models import Goal, Saving
from apps.users.models import User


@pytest.mark.django_db
def test_create_saving(test_user: User) -> None:
    saving = Saving.objects.create(
        operation_type="INFLOW",
        amount=500,
        user=test_user,
    )

    assert saving.operation_type == "INFLOW"
    assert saving.amount == 500


@pytest.mark.django_db
def test_create_goal(test_user: User) -> None:
    goal = Goal.objects.create(
        title="Test Goal",
        amount=500,
        user=test_user,
    )

    assert goal.title == "Test Goal"
    assert goal.amount == 500
