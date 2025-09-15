from dataclasses import dataclass
from decimal import Decimal

from apps.savings.models import Goal
from apps.savings.services.total_saved import calculate_total_saved


@dataclass
class GoalProgress:
    years_left: int
    months_left: int


def calculate_goal_progress(goal: Goal, monthly_savings: Decimal) -> GoalProgress:
    total_saved = calculate_total_saved(goal)

    remaining_amount = goal.amount - total_saved

    if remaining_amount <= 0:
        return GoalProgress(
            years_left=0,
            months_left=0,
        )

    months_left = (remaining_amount / monthly_savings).quantize(1)
    months_left = int(months_left)

    return GoalProgress(years_left=months_left // 12, months_left=months_left % 12)
