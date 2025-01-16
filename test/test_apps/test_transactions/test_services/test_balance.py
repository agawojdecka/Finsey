import pytest

from apps.transactions.models import Transaction
from apps.transactions.services.balance import get_balance
from apps.users.models import User


@pytest.mark.django_db
def test_get_balance():
    user = User.objects.create_user(username='test', password='1234')
    Transaction.objects.create(title='Test Income 1', transaction_type="INCOME", amount=1000, user=user)
    Transaction.objects.create(title='Test Income 2', transaction_type="INCOME", amount=500, user=user)
    Transaction.objects.create(title='Test Expense 1', transaction_type="EXPENSE", amount=400, user=user)
    Transaction.objects.create(title='Test Expense 2', transaction_type="EXPENSE", amount=100, user=user)

    balance = get_balance(user)

    expected_results = {
        "incomes": 1500,
        "expenses": 500,
        "balance": 1000
    }
    assert balance == expected_results
