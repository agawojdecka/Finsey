from typing import TYPE_CHECKING

from django.db.models import Sum

if TYPE_CHECKING:
    from apps.savings.models import Goal


def calculate_total_saved(goal: "Goal") -> float:
    from apps.savings.models import Saving

    total_inflow = (
        goal.savings.filter(
            operation_type=Saving.Types.INFLOW,
        ).aggregate(
            total_income=Sum('amount')
        )['total_income']
        or 0
    )

    total_outflow = (
        goal.savings.filter(
            operation_type=Saving.Types.OUTFLOW,
        ).aggregate(
            total_outflow=Sum('amount')
        )['total_outflow']
        or 0
    )

    total_saved = total_inflow - total_outflow

    return total_saved
