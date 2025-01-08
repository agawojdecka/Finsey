from django.db.models import Sum

from apps.transactions.models import Transaction


def get_balance(user):
    transactions = Transaction.objects.filter(user=user)
    incomes = transactions.filter(transaction_type=Transaction.Types.INCOME).aggregate(total=Sum('amount'))[
                  'total'] or 0
    expenses = transactions.filter(transaction_type=Transaction.Types.EXPENSE).aggregate(total=Sum('amount'))[
                   'total'] or 0

    balance = incomes - expenses

    return {
        "incomes": incomes,
        "expenses": expenses,
        "balance": balance
    }
