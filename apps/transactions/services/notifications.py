from datetime import timedelta
from logging import getLogger

from django.core.mail import EmailMessage
from django.db.models import Prefetch, Sum
from django.utils import timezone

from apps.core.utils.date import get_first_day_of_month
from apps.transactions.models import Transaction
from apps.users.models import User

logger = getLogger(__name__)


def send_monthly_balance_notification() -> None:
    """
    Calculates each user's incomes and expenses for the previous month,
    determines their balance, and emails a summary notification with
    an appropriate message based on the result.
    """
    current_date = timezone.now().date()

    last_day_of_settlement_period = get_first_day_of_month(current_date) - timedelta(days=1)
    first_day_of_settlement_period = last_day_of_settlement_period.replace(day=1)

    users = User.objects.prefetch_related(
        Prefetch(
            "transactions",
            queryset=Transaction.objects.filter(
                date__gte=first_day_of_settlement_period,
                date__lte=last_day_of_settlement_period,
            ),
        )
    )

    for user in users:
        monthly_incomes = (
            user.transactions.filter(transaction_type=Transaction.Types.INCOME).aggregate(total=Sum('amount'))['total']
            or 0
        )
        monthly_expenses = (
            user.transactions.filter(transaction_type=Transaction.Types.EXPENSE).aggregate(total=Sum('amount'))['total']
            or 0
        )
        monthly_balance = monthly_incomes - monthly_expenses

        if monthly_balance > 0:
            subject = "Congratulations, you have reached a positive monthly balance!"
        elif monthly_balance == 0:
            subject = "After all the expenses, we managed to break even!"
        else:
            subject = "Oops! Your monthly balance is below zero..."

        body = (
            f"Your monthly balance for period {first_day_of_settlement_period} "
            f"- {last_day_of_settlement_period} is {monthly_balance}."
        )
        from_email = "your-email@gmail.com"
        to_email = [user.email]

        email = EmailMessage(subject, body, from_email, to_email)

        try:
            email.send(fail_silently=False)
            logger.info(f"Notification sent successfully to user: {user.id}.")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
