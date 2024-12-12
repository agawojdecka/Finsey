import django_filters

from apps.savings.models import Saving, Goal


class SavingFilter(django_filters.FilterSet):
    operation_type = django_filters.ChoiceFilter(
        field_name="operation_type", choices=Saving.Types, lookup_expr="iexact"
    )
    goal = django_filters.ModelChoiceFilter(
        field_name="goal",
        queryset=Goal.objects.all(),
        to_field_name="title",
        label="Goal",
    )
    date = django_filters.DateFromToRangeFilter(field_name="date", label="Date (Range)")

    class Meta:
        model = Saving
        fields = ["operation_type", "goal", "date"]
