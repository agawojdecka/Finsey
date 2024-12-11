import django_filters

from apps.transactions.models import Transaction, Category


class TransactionFilter(django_filters.FilterSet):
    transaction_type = django_filters.ChoiceFilter(
        field_name="transaction_type", choices=Transaction.Types, lookup_expr="iexact"
    )
    category = django_filters.ModelChoiceFilter(
        field_name="category",
        queryset=Category.objects.all(),
        to_field_name="title",
        label="Category",
    )
    date = django_filters.DateFromToRangeFilter(field_name="date", label="Date (Range)")
    is_constant = django_filters.BooleanFilter(field_name="is_constant")

    class Meta:
        model = Transaction
        fields = ["transaction_type", "category", "date", "is_constant"]
