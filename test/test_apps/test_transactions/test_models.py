import pytest

from apps.transactions.models import Category, Transaction
from apps.users.models import User


@pytest.mark.django_db
def test_create_transaction() -> None:
    transaction = Transaction.objects.create(
        title="Salary",
        transaction_type="INCOME",
        amount=5000.00,
        user=User.objects.create_user(username="test", password="1234"),
    )

    assert transaction.title == "Salary"
    assert transaction.transaction_type == "INCOME"
    assert transaction.amount == 5000.00


@pytest.mark.django_db
def test_create_category() -> None:
    category = Category.objects.create(
        title="Salary",
        transaction_type="INCOME",
        user=User.objects.create_user(username="test", password="1234"),
    )

    assert category.title == "Salary"
    assert category.transaction_type == "INCOME"
