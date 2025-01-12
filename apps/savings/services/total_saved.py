from apps.savings.models import Saving


def calculate_total_saved(goal):
    total_saved = sum(
        saving.amount for saving in goal.savings.filter(operation_type=Saving.Types.INFLOW)
    ) - sum(
        saving.amount for saving in goal.savings.filter(operation_type=Saving.Types.OUTFLOW)
    )
    return total_saved