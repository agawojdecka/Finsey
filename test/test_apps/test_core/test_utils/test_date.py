from datetime import date

import pytest

from apps.core.utils.date import get_first_day_of_month, get_last_day_of_month


def test_get_first_day_of_month() -> None:
    day = date(2024, 2, 15)
    assert get_first_day_of_month(day) == date(2024, 2, 1)


@pytest.mark.parametrize(
    "day,expected_day",
    [
        (date(2024, 2, 15), date(2024, 2, 29)),
        (date(2024, 12, 1), date(2024, 12, 31)),
    ],
)
def test_get_last_day_of_month(day: date, expected_day: date) -> None:
    assert get_last_day_of_month(day) == expected_day
