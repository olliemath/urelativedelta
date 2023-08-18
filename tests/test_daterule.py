from __future__ import annotations

from datetime import date as pydate, datetime, timedelta

from urelativedelta import daterule, relativedelta


def test_date_rule_with_date():
    start = pydate(2020, 1, 1)

    # Seconds, hours, minutes etc
    for i, date in enumerate(daterule.secondly(start, count=24 * 60 * 60 * 2)):
        if i < 24 * 60 * 60:
            assert date == start, f"Expected {i} seconds to be on first day"
        else:
            assert date == start + timedelta(
                days=1
            ), f"Expected {i} seconds to be on second day"

    for i, date in enumerate(daterule.minutely(start, count=24 * 60 * 2)):
        if i < 24 * 60:
            assert date == start, f"Expected {i} minutes to be on first day"
        else:
            assert date == start + timedelta(
                days=1
            ), f"Expected {i} minutes to be on second day"

    for i, date in enumerate(daterule.hourly(start, count=24 * 2)):
        if i < 24:
            assert date == start, f"Expected {i} hours to be on first day"
        else:
            assert date == start + timedelta(
                days=1
            ), f"Expected {i} hours to be on second day"

    # Days, weeks
    days = list(daterule.daily(start, count=5))
    assert days[0] == start, "daterule.iterator should start at the initial day"
    assert days[1] == start + timedelta(
        days=1
    ), "daterule.iterator should increment in days"
    assert len(days) == 5, "daterule.iterator should finish before the count is up"

    finish = pydate(2020, 1, 29)
    weeks = list(daterule.weekly(start, end=finish))
    assert weeks[0] == start, "daterule.iterator should start at the initial day"
    assert weeks[1] == start + timedelta(
        days=7
    ), "daterule.iterator should increment in weeks"
    assert len(weeks) == 4, "daterule.iterator should finish before the final day"

    # Months, years
    interesting = pydate(2020, 1, 30)  # The day will change each month

    months = list(daterule.monthly(interesting, count=5))
    assert months[0] == interesting, "daterule.iterator should start at the initial day"
    assert months[1] == pydate(2020, 2, 29), "daterule.iterator should handle Feb"
    assert months[2] == pydate(2020, 3, 30), "daterule.iterator should not loose days"
    assert len(months) == 5, "daterule.iterator should finish before the count is up"

    years = list(daterule.yearly(interesting, count=3))
    assert years[0] == interesting, "daterule.iterator should start at the initial day"
    assert years[1] == pydate(
        2021, 1, 30
    ), "daterule.iterator should increment in years"
    assert len(years) == 3, "daterule.iterator should finish before the count is up"


def test_date_rule_with_datetime():
    # Seconds
    start = datetime(2020, 1, 1, 1, 2, 3)
    day = start.date()
    seconds_passed = 60 * 60 + 2 * 60 + 3

    for i, date in enumerate(daterule.secondly(start, count=24 * 60 * 60 * 2)):
        if i > 0:
            assert date > start, "Time should increase"

        if i < 24 * 60 * 60 - seconds_passed:
            assert date.date() == day
        elif i < 2 * 24 * 60 * 60 - seconds_passed:
            assert date.date() == day + timedelta(days=1)
        else:
            assert date.date() == day + timedelta(days=2)

    # Months
    interesting = datetime(2020, 1, 30, 1, 2, 3)  # The day will change each month
    months = list(daterule.monthly(interesting, count=5))

    assert months[0] == interesting
    assert months[1].date() == pydate(2020, 2, 29)
    assert months[1].time() == interesting.time()
    assert months[2].date() == pydate(
        2020, 3, 30
    ), "daterule.iterator should not loose days"
    assert months[2].time() == interesting.time()


def test_date_rule_edge_cases():
    start = pydate(2020, 1, 1)

    # Zero count
    dates = list(daterule.daily(start, count=0))
    assert dates == []

    # End equals start
    dates = list(daterule.daily(start, end=start))
    assert dates == []


def test_backwards_date_rule():
    start = pydate(2020, 3, 31)
    end = pydate(2019, 12, 31)
    freq = relativedelta(months=-1)

    dates1 = list(daterule.iterator(freq, start, count=3))
    assert dates1 == [pydate(2020, 3, 31), pydate(2020, 2, 29), pydate(2020, 1, 31)]

    dates2 = list(daterule.iterator(freq, start, end))
    assert dates1 == dates2


def test_long_running_rules():
    # Sanity tests for long-running shifts with various start months
    for month in (1, 3, 5, 7, 8, 10, 12):
        start = pydate(2020, month, 31)
        rule = daterule.monthly(start)

        for _ in range(120):
            shifted = next(rule)
            if shifted.month == 1:
                assert shifted.day == 31
            elif shifted.month == 4:
                assert shifted.day == 30

        freq = relativedelta(months=-1)
        rule = daterule.iterator(freq, start)

        for _ in range(120):
            shifted = next(rule)
            if shifted.month == 1:
                assert shifted.day == 31
            elif shifted.month == 4:
                assert shifted.day == 30
