from dateutil.relativedelta import relativedelta
from django.utils import timezone

from apps.transactions.models import PlannedTransaction, Transaction


def execute_planned_transactions() -> None:
    """
    Execute all planned transactions that have reached their scheduled time,
    create corresponding `Transaction` entries, mark executed plans
    as completed, and reschedule monthly payments for the next month.
    """
    today = timezone.now().date()

    planned_transactions = PlannedTransaction.objects.filter(scheduled_at__lte=today, is_executed=False)

    for planned_transaction in planned_transactions:
        Transaction.objects.create(
            title=planned_transaction.title,
            transaction_type=planned_transaction.transaction_type,
            amount=planned_transaction.amount,
            account=planned_transaction.account,
            category=planned_transaction.category,
            description=planned_transaction.description,
            user=planned_transaction.user,
        )

        if planned_transaction.is_monthly_payment:
            next_date = planned_transaction.scheduled_at + relativedelta(months=1)
            PlannedTransaction.objects.create(
                title=planned_transaction.title,
                transaction_type=planned_transaction.transaction_type,
                amount=planned_transaction.amount,
                account=planned_transaction.account,
                category=planned_transaction.category,
                description=planned_transaction.description,
                user=planned_transaction.user,
                scheduled_at=next_date,
                is_monthly_payment=True,
            )

        planned_transaction.is_executed = True
        planned_transaction.save(update_fields=["is_executed"])
