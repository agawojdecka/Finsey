from dataclasses import dataclass
from datetime import timedelta

from django.db.models import Sum

from apps.core.utils.date import get_current_date, get_first_day_of_month
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


def get_monthly_balance_for_all_users() -> dict:
    monthly_balances_dict = {}
    current_date = get_current_date()

    last_day_of_settlement_period = get_first_day_of_month(current_date) - timedelta(days=1)
    first_day_of_settlement_period = last_day_of_settlement_period.replace(day=1)

    users = User.objects.all()

    for user in users:
        monthly_income = Transaction.objects.filter(
            date__gte=first_day_of_settlement_period,
            date__lte=last_day_of_settlement_period,
            transaction_type=Transaction.Types.INCOME,
            user=user,
        ).aggregate(Sum('amount'))

        monthly_outcome = Transaction.objects.filter(
            date__gte=first_day_of_settlement_period,
            date__lte=last_day_of_settlement_period,
            transaction_type=Transaction.Types.EXPENSE,
            user=user,
        ).aggregate(Sum('amount'))

        income_sum = monthly_income['amount__sum'] or 0
        outcome_sum = monthly_outcome['amount__sum'] or 0
        balance = income_sum - outcome_sum

        monthly_balance = {user: balance}
        monthly_balances_dict.update(monthly_balance)

    return monthly_balances_dict


# TODO 1
# napisac funkcje ktora uzywajac .aggregate liczy sume wplywow (INCOME) dla wszystkich uzytkownikow i zwraca slownik
# dict[User, int]

# TODO 2
# napisac funkcje ktora uzywajac .aggregate liczy sume wplywow (EXPENSE) dla wszystkich uzytkownikow i zwraca slownik
# dict[User, int]

# TODO 3
# napisac funkcje ktora wywola funckje z TODO 1 i TODO 2 i zwroci
# dict[User, BalanceInfo]
