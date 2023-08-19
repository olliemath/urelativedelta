from __future__ import annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

if _TYPE_CHECKING:
    from datetime import date, datetime
    from typing import TypeVar

    D = TypeVar("D", date, datetime)


_THIRTY_DAY_MONTHS = {4, 6, 9, 11}


def is_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _normalise_day(year: int, month: int, day: int) -> int:
    """Shift the day backwards until it lies in the month.

    XXX: No attempt is made to handle days outside the 1-31 range.
    """
    if day <= 28:
        return day
    elif month == 2:
        return 28 + is_leap_year(year)
    elif day == 31 and (month == 4 or month == 6 or month == 9 or month == 11):
        return 30
    else:
        return day


def _shift_months_impl(
    year: int, month: int, day: int, months: int
) -> tuple[int, int, int]:
    """Shift a date by the given number of months.

    Ambiguous month-ends are shifted backwards as necessary."""
    year = year + (month + months - 1) // 12
    month = 1 + (month + months - 1) % 12

    # Inlining normalise day gives a nontrivial speed boost
    if day > 28:
        if month == 2:
            day = 28 + is_leap_year(year)
        elif day == 31 and month in _THIRTY_DAY_MONTHS:
            day = 30

    return year, month, day


def shift_months(date: D, months: int) -> D:
    """Shift a date by the given number of months.

    Ambiguous month-ends are shifted backwards as necessary."""
    year, month, day = _shift_months_impl(date.year, date.month, date.day, months)
    return date.replace(year=year, month=month, day=day)


def shift_years(date: D, years: int) -> D:
    """Shift a date by the given number of years.

    Ambiguous month-ends are shifted backwards as necessary."""
    return shift_months(date, years * 12)


def with_day(date: D, day: int) -> D:
    """Shift the date to have the given day.

    Ambiguous month-ends are shifted backwards as necessary.
    """
    return date.replace(day=_normalise_day(date.year, date.month, day))


def with_month(date: D, month: int) -> D:
    """Shift the date to have the given month.

    Ambiguous month-ends are shifted backwards as necessary.
    """
    if not 1 <= month <= 12:
        raise ValueError(f"month {month} should be between 1 and 12")

    return shift_months(date, month - date.month)


def with_year(date: D, year: int) -> D:
    """Shift the date to have the given year.

    Ambiguous month-ends are shifted backwards as necessary.
    """
    return shift_years(date, year - date.year)
