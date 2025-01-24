from apps.core.utils.date import *

def test_get_first_day_of_month():
    day = date(2024, 2,15)
    assert get_first_day_of_month(day) == date(2024, 2, 1)

def test_get_last_day_of_month():
    day_1 = date(2024, 2,15)
    day_2 = date(2024, 12,1)
    assert get_last_day_of_month(day_1) == date(2024, 2, 29)
    assert get_last_day_of_month(day_2) == date(2024, 12, 31)
