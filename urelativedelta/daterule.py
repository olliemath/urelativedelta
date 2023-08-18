"""Provides iterators yielding datetimes with a regular interval.

Examples
--------
Yield dates on Feb 29th every year (or else Feb 28th if not a leap year), starting on Feb 28th 2005
and finishing on Feb 28th 2007:
>>> start = date(2003, 2, 28)
>>> end = date(2006, 2, 28)
>>> freq = relativedelta(years=1)
>>> list(daterule.iteartor(freq, start=start, end=end, rolling_day=29))
[date(2003, 2, 28), date(2004, 2, 29), date(2005, 2, 28)]

Yield 4 dates, one each month, from Jan 31st 2020:
>>> start = date(2020, 1, 30)
>>> list(daterule.monthly(start, count=4))
[date(2020, 1, 31), date(2020, 2, 29), date(2020, 3, 31), date(2020, 4, 30)]

Warnings
--------
You can easily get an infinite series of dates by specifying a negative relativedelta
and an end date in the future.

When using `rolling_day` with timedeltas it is possible to get unintuitive behaviour.
For example, the following would cycle through Jan 1st 2020 for 62 datetimes, then
switch to Feb 1st 2020 for the next 58, etc:
>>> start = datetime(2020, 1, 1)
>>> freq = timedelta(hours=12)
>>> for date in daterule.iterator(freq, start):
        print(date.isoformat())
2020-01-01T00:00:00
2020-01-01T12:00:00
2020-01-01T00:00:00
2020-01-01T12:00:00
2020-01-01T00:00:00
...
2020-02-01T00:00:00
2020-02-01T12:00:00
2020-02-01T00:00:00
2020-02-01T12:00:00
2020-02-01T00:00:00
...
"""
from __future__ import annotations

from datetime import timedelta as _timedelta
from typing import TYPE_CHECKING as _TYPE_CHECKING

from .relativedelta import relativedelta as _relativedelta
from .utils import with_day as _with_day

if _TYPE_CHECKING:
    from collections.abc import Iterator
    from datetime import date, datetime
    from typing import TypeVar, Union

    D = TypeVar("D", datetime, date)
    deltalike = Union[_relativedelta, _timedelta]


def iterator(
    freq: deltalike,
    start: D,
    end: D | None = None,
    count: int | None = None,
    rolling_day: int | None = None,
) -> Iterator[D]:
    """An iterator yielding datetimes with a regular interval.

    Parameters
    ----------
    freq : relativedelta or timedelta
        The interval to shift successive dates by.
    start : datetime or date
        The startpoint (inclusive) for yielding dates.
    end : optional datetime or date
        The endpoint (exclusive) beyond which we should no longer yield dates.
    count: optional int
        The number of dates to yield.
    rolling_day: optional int
        The target day for new dates.

    Yields
    ------
    datetime or date
        The dates in the sequence for the provided rule.
    """
    if isinstance(freq, _timedelta):
        freq = _relativedelta(timedelta=freq)

    current_count = 0

    while True:
        if count is not None and current_count >= count:
            return

        current_date = start + freq * current_count
        if rolling_day is not None:
            current_date = _with_day(current_date, rolling_day)

        if end is not None:
            if end >= start and current_date >= end:
                return
            if end < start and current_date <= end:
                return

        current_count += 1
        yield current_date


def secondly(
    start: D,
    end: D | None = None,
    count: int | None = None,
) -> Iterator[D]:
    """An iterator yielding datetimes once per second.

    Parameters
    ----------
    start : datetime or date
        The startpoint (inclusive) for yielding dates.
    end : optional datetime or date
        The endpoint (exclusive) beyond which we should no longer yield dates.
    count: optional int
        The number of dates to yield.

    Yields
    ------
    datetime or date
        The dates in the sequence for the provided rule.
    """
    freq = _relativedelta(seconds=1)
    return iterator(freq, start, end, count)


def minutely(
    start: D,
    end: D | None = None,
    count: int | None = None,
) -> Iterator[D]:
    """An iterator yielding datetimes once per minute.

    Parameters
    ----------
    start : datetime or date
        The startpoint (inclusive) for yielding dates.
    end : optional datetime or date
        The endpoint (exclusive) beyond which we should no longer yield dates.
    count: optional int
        The number of dates to yield.

    Yields
    ------
    datetime or date
        The dates in the sequence for the provided rule.
    """
    freq = _relativedelta(minutes=1)
    return iterator(freq, start, end, count)


def hourly(
    start: D,
    end: D | None = None,
    count: int | None = None,
) -> Iterator[D]:
    """An iterator yielding datetimes once per hour.

    Parameters
    ----------
    start : datetime or date
        The startpoint (inclusive) for yielding dates.
    end : optional datetime or date
        The endpoint (exclusive) beyond which we should no longer yield dates.
    count: optional int
        The number of dates to yield.

    Yields
    ------
    datetime or date
        The dates in the sequence for the provided rule.
    """
    freq = _relativedelta(hours=1)
    return iterator(freq, start, end, count)


def daily(
    start: D,
    end: D | None = None,
    count: int | None = None,
) -> Iterator[D]:
    """An iterator yielding datetimes once per day.

    Parameters
    ----------
    start : datetime or date
        The startpoint (inclusive) for yielding dates.
    end : optional datetime or date
        The endpoint (exclusive) beyond which we should no longer yield dates.
    count: optional int
        The number of dates to yield.

    Yields
    ------
    datetime or date
        The dates in the sequence for the provided rule.
    """
    freq = _relativedelta(days=1)
    return iterator(freq, start, end, count)


def weekly(
    start: D,
    end: D | None = None,
    count: int | None = None,
) -> Iterator[D]:
    """An iterator yielding datetimes once per week.

    Parameters
    ----------
    start : datetime or date
        The startpoint (inclusive) for yielding dates.
    end : optional datetime or date
        The endpoint (exclusive) beyond which we should no longer yield dates.
    count: optional int
        The number of dates to yield.

    Yields
    ------
    datetime or date
        The dates in the sequence for the provided rule.
    """
    freq = _relativedelta(days=7)
    return iterator(freq, start, end, count)


def monthly(
    start: D,
    end: D | None = None,
    count: int | None = None,
    rolling_day: int | None = None,
) -> Iterator[D]:
    """An iterator yielding datetimes once per month.

    Parameters
    ----------
    start : datetime or date
        The startpoint (inclusive) for yielding dates.
    end : optional datetime or date
        The endpoint (exclusive) beyond which we should no longer yield dates.
    count: optional int
        The number of dates to yield.
    rolling_day: optional int
        The target day for new dates.

    Yields
    ------
    datetime or date
        The dates in the sequence for the provided rule.
    """
    freq = _relativedelta(months=1)
    return iterator(freq, start, end, count, rolling_day)


def yearly(
    start: D,
    end: D | None = None,
    count: int | None = None,
    rolling_day: int | None = None,
) -> Iterator[D]:
    """An iterator yielding datetimes once per year.

    Parameters
    ----------
    start : datetime or date
        The startpoint (inclusive) for yielding dates.
    end : optional datetime or date
        The endpoint (exclusive) beyond which we should no longer yield dates.
    count: optional int
        The number of dates to yield.
    rolling_day: optional int
        The target day for new dates.

    Yields
    ------
    datetime or date
        The dates in the sequence for the provided rule.
    """
    freq = _relativedelta(years=1)
    return iterator(freq, start, end, count, rolling_day)
