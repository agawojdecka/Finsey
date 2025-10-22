from datetime import date

from dateutil.relativedelta import relativedelta


def get_first_day_of_month(day: date) -> date:
    """Return the first day of the month from the given date."""
    return day.replace(day=1)


def get_last_day_of_month(day: date) -> date:
    """Return the last day of the month from the given date."""
    return day + relativedelta(day=31)


def get_current_date() -> date:
    """Return the last day of the month from the given date."""
    return date.today()
