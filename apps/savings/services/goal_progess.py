from apps.savings.services.total_saved import calculate_total_saved


def calculate_goal_progress(goal, monthly_savings):
    total_saved = calculate_total_saved(goal)

    remaining_amount = goal.amount - total_saved

    if remaining_amount <= 0:
        return {"months_left": 0, "message": "Goal already completed."}

    months_left = (remaining_amount / monthly_savings).quantize(1)
    months_left = int(months_left)

    if months_left >= 12:
        years = months_left // 12
        months = months_left % 12
        return {
            "years_left": years,
            "months_left": months
        }
    else:
        return {"months_left": months_left}
