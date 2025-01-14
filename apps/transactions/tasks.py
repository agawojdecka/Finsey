from celery import shared_task

from apps.transactions.services.report import generate_and_send_report


@shared_task
def generate_and_send_report_task(user_id, selected_columns):
    print(f"Generating report for user_id: {user_id}")
    generate_and_send_report(user_id, selected_columns)
    print(f"Transactions report for user {user_id} created successfully.")
