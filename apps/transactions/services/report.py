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
    "is_constant",
]


def generate_report(user_id, selected_columns):
    user = User.objects.get(id=user_id)

    wb = Workbook(f'Report.xlsx')
    ws = wb.add_worksheet()

    valid_columns = [column_name for column_name in selected_columns if column_name in AVAILABLE_REPORT_FIELDS]

    for col_num, column in enumerate(valid_columns):
        ws.write(0, col_num, column)

    transactions = Transaction.objects.filter(user=user)

    for row_num, transaction in enumerate(transactions, start=1):
        for col_num, column in enumerate(valid_columns):
            value = getattr(transaction, column)
            ws.write(row_num, col_num, str(value) if value else '')

    wb.close()
