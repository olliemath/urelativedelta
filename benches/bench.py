from __future__ import annotations

import sys
from datetime import datetime, timedelta
from timeit import timeit

from dateutil.relativedelta import relativedelta as du_delta

from urelativedelta import relativedelta

klass = sys.argv[1]


dates = [datetime(2000, 1, 1) + timedelta(days=n) for n in range(5_000)]


def do_shifts():
    if klass == "relativedelta":
        for d in dates:
            d + relativedelta(years=100)
    if klass == "dateutil":
        for d in dates:
            d + du_delta(years=100)


print(klass, timeit(do_shifts, number=1000))
