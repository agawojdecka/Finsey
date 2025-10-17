from datetime import timedelta

import pytest
from django.utils import timezone

from apps.accounts.models import Account
from apps.transactions.models import Category, PlannedTransaction, Transaction
from apps.users.models import User


@pytest.mark.django_db
def test_create_transaction() -> None:
    user = User.objects.create_user(username="test", password="1234")

    account = Account.objects.create(
        account_type="MAIN",
        name="Test",
        user=user,
    )

    transaction = Transaction.objects.create(
        account=account,
        title="Salary",
        transaction_type="INCOME",
        amount=5000.00,
        user=user,
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


@pytest.mark.django_db
def test_create_planned_transaction() -> None:
    user = User.objects.create_user(username="test", password="1234")

    account = Account.objects.create(
        account_type="MAIN",
        name="Test",
        user=user,
    )

    planned_transaction = PlannedTransaction.objects.create(
        account=account,
        title="Test",
        amount=100.00,
        user=user,
        scheduled_at=timezone.now() + timedelta(days=1),
    )

    assert planned_transaction.title == "Test"
    assert planned_transaction.amount == 100.00
