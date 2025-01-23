from celery import shared_task

from apps.transactions.services.report import generate_and_send_report, generate_monthly_expense_report
from apps.transactions.services.notifications import send_monthly_balance_notification


@shared_task
def generate_and_send_report_task(user_id, selected_columns):
    print(f"Generating report for user_id: {user_id}")
    generate_and_send_report(user_id, selected_columns)
    print(f"Transactions report for user {user_id} created successfully.")


@shared_task
def generate_monthly_expense_report_task(user_id):
    print(f"Generating monthly expense report for user_id: {user_id}")
    generate_monthly_expense_report(user_id)
    print(f"Monthly expense report for user {user_id} created successfully.")


@shared_task
def send_monthly_balance_notification_task():
    send_monthly_balance_notification()