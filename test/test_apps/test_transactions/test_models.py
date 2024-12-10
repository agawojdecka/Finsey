import pytest
from apps.transactions.models import Transaction


@pytest.mark.django_db
def test_create_transaction():
    transaction = Transaction.objects.create(
        title="Salary",
        transaction_type="INCOME",
        amount=5000.00,
    )

    assert transaction.title == "Salary"
    assert transaction.transaction_type == "INCOME"
    assert transaction.amount == 5000.00
