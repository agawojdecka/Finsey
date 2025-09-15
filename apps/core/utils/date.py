from datetime import date, timedelta


def get_first_day_of_month(day: date) -> date:
    return day.replace(day=1)


def get_last_day_of_month(day: date) -> date:
    if day.month == 12:
        return day.replace(day=31)
    return day.replace(month=day.month + 1, day=1) - timedelta(days=1)
