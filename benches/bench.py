from __future__ import annotations

import random
import sys
from datetime import datetime, timedelta
from timeit import timeit

import dateutil.relativedelta

import urelativedelta

random.seed(12345)
KLASS = sys.argv[1]
NUMDATES = 5_000

dates = [datetime(2000, 1, 1) + timedelta(days=n) for n in range(NUMDATES)]
shuffled = list(dates)
random.shuffle(shuffled)


def do_combined():
    if KLASS == "urelativedelta":
        for d in dates:
            d + urelativedelta.relativedelta(years=100)
    if KLASS == "dateutil":
        for d in dates:
            d + dateutil.relativedelta.relativedelta(years=100)


def do_shifts():
    if KLASS == "urelativedelta":
        delta = urelativedelta.relativedelta(years=100)
        for d in dates:
            d + delta
    if KLASS == "dateutil":
        delta = dateutil.relativedelta.relativedelta(years=100)
        for d in dates:
            d + delta


def do_inits():
    if KLASS == "urelativedelta":
        for _ in range(NUMDATES):
            urelativedelta.relativedelta(years=10, months=10, days=10)
    if KLASS == "dateutil":
        for _ in range(NUMDATES):
            dateutil.relativedelta.relativedelta(years=10, months=10, days=10)


def do_difference_inits():
    if KLASS == "urelativedelta":
        for d1, d2 in zip(shuffled, shuffled, strict=False):
            urelativedelta.relativedelta.difference(d1, d2)
    if KLASS == "dateutil":
        for d1, d2 in zip(shuffled, shuffled, strict=False):
            dateutil.relativedelta.relativedelta(d1, d2)


print(f"{KLASS} combined:", timeit(do_combined, number=1000))
print(f"{KLASS} shifts:", timeit(do_shifts, number=1000))
print(f"{KLASS} inits:", timeit(do_inits, number=1000))
print(f"{KLASS} differences:", timeit(do_difference_inits, number=1000))
