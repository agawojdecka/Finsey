import pytest

from apps.accounts.models import Account
from apps.users.models import User


@pytest.mark.django_db
def test_create_account(test_user: User) -> None:
    account = Account.objects.create(
        account_type="MAIN",
        name="Test",
        currency="USD",
        user=test_user,
    )

    assert account.account_type == "MAIN"
    assert account.name == "Test"
    assert account.currency == "USD"
    assert len(account.account_number) == 36
