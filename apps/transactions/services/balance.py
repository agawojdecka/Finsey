from dataclasses import dataclass

from django.db.models import Sum

from apps.transactions.models import Transaction
from apps.users.models import User


@dataclass
class BalanceInfo:
    income: float
    expense: float
    balance: float


def get_balance(user: User) -> BalanceInfo:
    """
    Returns balance of all incomes and outcomes for given user.
    """
    transactions = Transaction.objects.filter(user=user)
    income_sum = (
        transactions.filter(transaction_type=Transaction.Types.INCOME).aggregate(total=Sum('amount'))['total'] or 0
    )
    expense_sum = (
        transactions.filter(transaction_type=Transaction.Types.EXPENSE).aggregate(total=Sum('amount'))['total'] or 0
    )

    balance = income_sum - expense_sum

    return BalanceInfo(income=income_sum, expense=expense_sum, balance=balance)
