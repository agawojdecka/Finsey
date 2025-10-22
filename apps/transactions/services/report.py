from django.core.mail import EmailMessage
from django.utils.timezone import now
from xlsxwriter import Workbook

from apps.transactions.models import Transaction
from apps.users.models import User

AVAILABLE_REPORT_FIELDS = [
    "id",
    "title",
    "transaction_type",
    "amount",
    "category",
    "date",
    "description",
]


def generate_and_send_report(user_id: int, selected_columns: list[str]) -> None:
    """
    Generate an Excel report filtered by the columns selected by the user,
    including all transactions of a given user, and send it via email
    to the recipient.
    """
    user = User.objects.get(id=user_id)

    valid_columns = [column_name for column_name in selected_columns if column_name in AVAILABLE_REPORT_FIELDS]

    with Workbook("Report.xlsx") as wb:
        ws = wb.add_worksheet()

        for col_num, column in enumerate(valid_columns):
            ws.write(0, col_num, column)

        transactions = Transaction.objects.filter(user=user)
        for row_num, transaction in enumerate(transactions, start=1):
            for col_num, column in enumerate(valid_columns):
                value = getattr(transaction, column)
                ws.write(row_num, col_num, str(value) if value else "")

    subject = 'Report of transactions'
    body = 'This is a report of your transactions.'
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


def generate_monthly_expense_report(user_id: int) -> None:
    """
    Generate an Excel report of the user's expenses for the current month,
    including a total expense summary at the end.
    """
    user = User.objects.get(id=user_id)

    current_date = now()
    current_year = current_date.year
    current_month = current_date.month

    transactions = Transaction.objects.filter(
        user=user,
        transaction_type="EXPENSE",
        date__month=current_month,
        date__year=current_year,
    )

    with Workbook("Monthly_expense_report.xlsx") as wb:
        ws = wb.add_worksheet()

        for col_num, column in enumerate(AVAILABLE_REPORT_FIELDS):
            ws.write(0, col_num, column)

        for row_num, transaction in enumerate(transactions, start=1):
            for col_num, column in enumerate(AVAILABLE_REPORT_FIELDS):
                value = getattr(transaction, column)
                ws.write(row_num, col_num, str(value) if value else "")

        total_amount = sum(transaction.amount for transaction in transactions)
        last_row = len(transactions) + 1
        amount_col_index = AVAILABLE_REPORT_FIELDS.index("amount")

        ws.write(last_row, 0, "Total expenses")
        ws.write(last_row, amount_col_index, total_amount)
