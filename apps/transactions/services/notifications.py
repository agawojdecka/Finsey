from datetime import timedelta
from logging import getLogger

from django.core.mail import EmailMessage

from apps.core.utils.date import get_current_date, get_first_day_of_month
from apps.transactions.services.balance import get_monthly_balance_for_all_users

logger = getLogger(__name__)


def send_monthly_balance_notification() -> None:
    """
    Sends last month's balance notifications to all users
    with appropriate message based on the result.
    """
    current_date = get_current_date()

    last_day_of_settlement_period = get_first_day_of_month(current_date) - timedelta(days=1)
    first_day_of_settlement_period = last_day_of_settlement_period.replace(day=1)

    monthly_balances_dict = get_monthly_balance_for_all_users()

    for user, monthly_balance in monthly_balances_dict.items():

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
