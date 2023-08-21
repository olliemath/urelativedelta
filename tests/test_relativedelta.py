from __future__ import annotations

from datetime import date, datetime, timedelta

import dateutil.relativedelta
import pytest
from hypothesis import given, strategies as st

from urelativedelta import relativedelta

MIND = datetime(1600, 1, 1)
MAXD = datetime(3000, 1, 1)


def test_duration_arithmetic():
    x = relativedelta(months=5 * 12 + 7, seconds=100)
    y = relativedelta(months=3 * 12 + 6, seconds=300)
    z = timedelta(days=100)

    assert x + y == relativedelta(months=9 * 12 + 1, seconds=400)
    assert x - y == relativedelta(months=2 * 12 + 1, seconds=-200)
    assert x + z == relativedelta(months=5 * 12 + 7, days=100, seconds=100)
    assert y + x == y + x, "Addition should be symmetric"
    assert x - y == -(y - x), "Subtraction should be anti-symmetric"
    assert y + z == z + y, "Addition should be symmetric"
    assert y - z == -(z - y), "Subtraction should be anti-symmetric"

    assert x // 2 == relativedelta(months=5 * 6 + 3, seconds=50)
    assert x * 2 == relativedelta(months=10 * 12 + 14, seconds=200)
    assert 2 * x == x * 2, "Multiplication should be symmetric"

    # Dividing a 1-month by e.g. 2 has no unambiguous meaning
    with pytest.raises(TypeError, match="unsupported operand"):
        x / 2


def test_date_arithmetic():
    base = date(2020, 2, 29)

    assert base + relativedelta(months=24) == date(2022, 2, 28)
    assert base + relativedelta(months=48) == date(2024, 2, 29)

    assert base - relativedelta(months=24) == date(2018, 2, 28)
    assert base - relativedelta(months=48) == date(2016, 2, 29)

    not_leap = date(2020, 2, 28)
    tricky_delta = relativedelta(months=24, days=1)
    assert base + tricky_delta == date(2022, 3, 1)
    assert base + tricky_delta == not_leap + tricky_delta

    tricky_delta = relativedelta(months=24, days=-1)
    assert base - tricky_delta == date(2018, 3, 1)
    assert base - tricky_delta == not_leap - tricky_delta


def test_differences():
    # Later day of month -> last day of month counts as 1 month shift
    d1 = date(2020, 2, 29)

    d2 = date(2020, 1, 31)
    assert relativedelta.difference(d1, d2) == relativedelta(months=1)

    d2 = date(2020, 1, 30)
    assert relativedelta.difference(d1, d2) == relativedelta(months=1)

    d2 = date(2020, 1, 29)
    assert relativedelta.difference(d1, d2) == relativedelta(months=1)

    # Earlier day of month -> later day of month counts as day shift
    d2 = date(2020, 1, 28)
    assert relativedelta.difference(d1, d2) == relativedelta(months=1, days=1)

    # Later day of month -> not last day of month counts as day shift
    d1 = date(2020, 2, 28)
    d2 = date(2020, 1, 31)
    assert relativedelta.difference(d1, d2) == relativedelta(days=28)

    d2 = date(2020, 1, 30)
    assert relativedelta.difference(d1, d2) == relativedelta(days=29)


def test_differences_negative():
    d1 = date(2020, 2, 29)
    d2 = date(2020, 3, 31)

    assert relativedelta.difference(d1, d2) == relativedelta(months=-1)

    d1 = date(2020, 2, 28)
    assert relativedelta.difference(d1, d2) == relativedelta(months=-1, days=-1)

    d1 = date(2020, 2, 29)
    d2 = date(2020, 3, 30)
    assert relativedelta.difference(d1, d2) == relativedelta(months=-1)

    d1 = date(2020, 2, 29)
    d2 = date(2020, 3, 29)
    assert relativedelta.difference(d1, d2) == relativedelta(months=-1)

    d1 = date(2020, 2, 29)
    d2 = date(2020, 3, 28)
    assert relativedelta.difference(d1, d2) == relativedelta(days=-28)


@given(st.datetimes(), st.datetimes())
def test_difference_spans_gap(d1, d2):
    delta = relativedelta.difference(d1, d2)
    assert d2 + delta == d1


# Prevent overflows with adding deltas to dates
_restricted_dates = st.datetimes(
    min_value=datetime(1600, 1, 1), max_value=datetime(3000, 1, 1)
)


@given(_restricted_dates, _restricted_dates, _restricted_dates)
def test_difference_against_dateutil(d1, d2, d3):
    expected = dateutil.relativedelta.relativedelta(d1, d2)
    actual = relativedelta.difference(d1, d2)

    assert actual.total_months == 12 * expected.years + expected.months
    assert d3 + actual == d3 + expected


def test_difference_with_nones():
    # This is only here for compatability with dateutil
    assert relativedelta.difference(date(2020, 1, 1), None) == relativedelta()
    assert relativedelta.difference(None, date(2020, 1, 1)) == relativedelta()
    assert relativedelta.difference(None, None) == relativedelta()
