from celery import shared_task

from apps.transactions.services.report import generate_report


@shared_task
def create_report(user_id, selected_columns):
    print(f"Generating report for user_id: {user_id}")
    generate_report(user_id, selected_columns)
    print(f"Transactions report for user {user_id} created successfully.")
