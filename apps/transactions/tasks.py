from celery import shared_task
from django.core.mail import EmailMessage

from apps.transactions.services.report import generate_report


@shared_task
def create_report(user_id, selected_columns):
    print(f"Generating report for user_id: {user_id}")
    generate_report(user_id, selected_columns)
    print(f"Transactions report for user {user_id} created successfully.")


@shared_task
def send_mail_with_report():
    subject = 'Hello from Django with Attachment'
    body = 'This is a test email with an attachment.'
    from_email = 'your-email@gmail.com'
    to_email = ['recipient@example.com']

    email = EmailMessage(subject, body, from_email, to_email)

    file_path = 'Report.xlsx'
    try:
        email.attach_file(file_path)
        email.send(fail_silently=False)
        print("Email sent successfully with attachment!")
    except Exception as e:
        print(f"Failed to send email: {e}")
