from __future__ import annotations

from datetime import date, timedelta

import pytest

from relativedelta import relativedelta


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
