from celery import shared_task

from apps.transactions.services.notifications import send_monthly_balance_notification
from apps.transactions.services.planned_transactions import execute_planned_transactions
from apps.transactions.services.report import (
    generate_and_send_report,
    generate_monthly_expense_report,
)


@shared_task
def generate_and_send_report_task(user_id: int, selected_columns: list[str]) -> None:
    generate_and_send_report(user_id, selected_columns)


@shared_task
def generate_monthly_expense_report_task(user_id: int) -> None:
    generate_monthly_expense_report(user_id)


@shared_task
def send_monthly_balance_notification_task() -> None:
    send_monthly_balance_notification()


@shared_task
def execute_planned_transactions_task() -> None:
    execute_planned_transactions()
