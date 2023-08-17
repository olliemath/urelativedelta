from __future__ import annotations

from datetime import date, datetime

import pytest

from relativedelta import is_leap_year, shift_months, shift_years, with_month, with_year

LEAP_YEARS_1900_TO_2020 = frozenset(
    (
        1904,
        1908,
        1912,
        1916,
        1920,
        1924,
        1928,
        1932,
        1936,
        1940,
        1944,
        1948,
        1952,
        1956,
        1960,
        1964,
        1968,
        1972,
        1976,
        1980,
        1984,
        1988,
        1992,
        1996,
        2000,
        2004,
        2008,
        2012,
        2016,
        2020,
    )
)


@pytest.mark.parametrize("year", range(1900, 2021))
def test_leap_year_cases(year: int):
    assert is_leap_year(year) == (year in LEAP_YEARS_1900_TO_2020)


@pytest.mark.parametrize(
    ("shift", "expected"),
    [
        (0, date(2020, 1, 31)),
        (1, date(2020, 2, 29)),
        (2, date(2020, 3, 31)),
        (3, date(2020, 4, 30)),
        (4, date(2020, 5, 31)),
        (5, date(2020, 6, 30)),
        (6, date(2020, 7, 31)),
        (7, date(2020, 8, 31)),
        (8, date(2020, 9, 30)),
        (9, date(2020, 10, 31)),
        (10, date(2020, 11, 30)),
        (11, date(2020, 12, 31)),
        (12, date(2021, 1, 31)),
        (13, date(2021, 2, 28)),
        (-1, date(2019, 12, 31)),
        (-2, date(2019, 11, 30)),
        (-3, date(2019, 10, 31)),
        (-4, date(2019, 9, 30)),
        (-5, date(2019, 8, 31)),
        (-6, date(2019, 7, 31)),
        (-7, date(2019, 6, 30)),
        (-8, date(2019, 5, 31)),
        (-9, date(2019, 4, 30)),
        (-10, date(2019, 3, 31)),
        (-11, date(2019, 2, 28)),
        (-12, date(2019, 1, 31)),
        (-13, date(2018, 12, 31)),
        (1265, date(2125, 6, 30)),
    ],
)
def test_shift_months(shift: int, expected: date):
    base = date(2020, 1, 31)
    assert shift_months(base, shift) == expected


@pytest.mark.parametrize(
    ("shift", "expected"),
    [
        (0, date(2020, 12, 31)),
        (1, date(2021, 1, 31)),
        (2, date(2021, 2, 28)),
        (12, date(2021, 12, 31)),
        (18, date(2022, 6, 30)),
        (-1, date(2020, 11, 30)),
        (-2, date(2020, 10, 31)),
        (-10, date(2020, 2, 29)),
        (-12, date(2019, 12, 31)),
        (-18, date(2019, 6, 30)),
    ],
)
def test_shift_months_with_overflow(shift: int, expected: date):
    base = date(2020, 12, 31)
    assert shift_months(base, shift) == expected


def test_shift_months_datetime():
    base = datetime(2020, 1, 31, 1, 2, 3)
    assert shift_months(base, 0) == base
    assert shift_months(base, 1) == datetime(2020, 2, 29, 1, 2, 3)
    assert shift_months(base, 2) == datetime(2020, 3, 31, 1, 2, 3)


@pytest.mark.parametrize(
    ("shift", "expected"),
    [
        (0, date(2020, 2, 29)),
        (1, date(2021, 2, 28)),
        (4, date(2024, 2, 29)),
        (80, date(2100, 2, 28)),
        (-1, date(2019, 2, 28)),
        (-4, date(2016, 2, 29)),
        (-20, date(2000, 2, 29)),
        (-120, date(1900, 2, 28)),
    ],
)
def test_shift_years(shift: int, expected: date):
    base = date(2020, 2, 29)
    assert shift_years(base, shift) == expected


def test_with_month_special_cases():
    with pytest.raises(ValueError, match="0"):
        with_month(date(2020, 1, 31), 0)

    with pytest.raises(ValueError, match="13"):
        with_month(date(2020, 1, 31), 13)

    # Forward shifts work
    assert with_month(date(2021, 1, 31), 2) == date(2021, 2, 28)
    # Backwards shifts work too
    assert with_month(date(2021, 3, 30), 2) == date(2021, 2, 28)


@pytest.mark.parametrize(
    ("month", "expected"),
    [
        (1, date(2020, 1, 31)),
        (2, date(2020, 2, 29)),
        (3, date(2020, 3, 31)),
        (4, date(2020, 4, 30)),
        (5, date(2020, 5, 31)),
        (6, date(2020, 6, 30)),
        (7, date(2020, 7, 31)),
        (8, date(2020, 8, 31)),
        (9, date(2020, 9, 30)),
        (10, date(2020, 10, 31)),
        (11, date(2020, 11, 30)),
        (12, date(2020, 12, 31)),
    ],
)
def test_with_month(month: int, expected: date):
    base = date(2020, 1, 31)
    assert with_month(base, month) == expected


@pytest.mark.parametrize(
    ("year", "expected"),
    [
        (2024, date(2024, 2, 29)),
        (2021, date(2021, 2, 28)),
        (2020, date(2020, 2, 29)),
        (2019, date(2019, 2, 28)),
        (2016, date(2016, 2, 29)),
    ],
)
def test_with_year(year: int, expected: date):
    base = date(2020, 2, 29)
    assert with_year(base, year) == expected
