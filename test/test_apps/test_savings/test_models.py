import pytest

from apps.savings.models import Goal, Saving
from apps.users.models import User


@pytest.mark.django_db
def test_create_saving() -> None:
    saving = Saving.objects.create(
        operation_type="INFLOW",
        amount=500,
        user=User.objects.create_user(username="test", password="1234"),
    )

    assert saving.operation_type == "INFLOW"
    assert saving.amount == 500


@pytest.mark.django_db
def test_create_goal() -> None:
    goal = Goal.objects.create(
        title="Test Goal",
        amount=500,
        user=User.objects.create_user(username="test", password="1234"),
    )

    assert goal.title == "Test Goal"
    assert goal.amount == 500
