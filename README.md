# [uRelativeDelta][pypi]

A small fast implementation of relativedelta

[![urelativedelta GitHub Actions][gh-image]][gh-checks]
[![urelativedelta on PyPI][pypi-image]][pypi]
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[gh-image]: https://github.com/olliemath/urelativedelta/workflows/test/badge.svg
[gh-checks]: https://github.com/olliemath/urelativedelta/actions?query=workflow%3Atest
[pypi-image]: https://img.shields.io/pypi/v/urelativedelta
[pypi]: https://pypi.org/project/urelativedelta/

urelativedelta provides the following utilities:

- `relativedelta` a simple replacement for [dateutil.relativedelta](https://dateutil.readthedocs.io/en/stable/relativedelta.html)
- `daterule`: a module of useful iterators yielding regular (e.g. monthly) dates
- proceedural helper functions for shifting date and datetime values by months and years

it is a python port of the [chronoutil](https://github.com/olliemath/chronoutil) library for rust (itself inspired by [dateutil](https://pypi.org/project/python-dateutil)).


## Benchmarks

Originally urelativedelta was used for speeding up complicated cashflow bucketing
computations (where there are lots of relativedeltas). It's pretty successful:

| benchmark | interpreter | urelativedelta | python-dateutil | speedup |
| ------ | ------ | ------ | ------ | ------ |
| shift 5mn dates by 100 years | cpython 3.11 | 6.04s | 20.44s | 3.38x |
| shift 5mn dates by 100 years | pypy 3.9 | 0.37s | 3.17s | 8.57x |
| subtract 5mn date pairs | cpython 3.11 | 6.73s | 17.77s | 2.64x |
| subtract 5mn date pairs | pypy 3.9 | 1.20s | 3.30s | 2.74x |

all of which means that using pypy and switching libraries can buy you a ~50x speed improvement!


## Usage

Install via:

```bash
pip install urelativedelta
```

then you can run

```python
from datetime import datetime
from urelativedelta import relativedelta

delta = relativedelta(years=1, months=1, days=1, hours=1)
datetime(2050, 1, 1) + delta
```

## Overview

### relativedelta

urelativedelta uses a **`relativedelta`** type to represent the magnitude of a time span
which may not be absolute (i.e. which is not simply a fixed number of nanoseconds).
A relativedelta is made up of a number of months together with an absolute `timedelta`
component.

```python
delta = relativedelta(months=1, days=1)
start = datetime(2020, 1, 1)
assert start + delta == datetime(2020, 2, 2)
```

You can also initialise a relativedelta as the difference between
two datetimes using its `difference` method:

```python
delta = relativedelta.difference(date(2020, 2, 29), date(2020, 1, 30))
assert delta == relativedelta(months=1)
```

The behaviour of `relativedelta` is consistent and well-defined in edge-cases
(see the Design decisions section for an explanation):

```python
delta = relativedelta(months=1, days=1)
start = date(2020, 1, 30)
assert start + delta == date(2020, 3, 1)
```

### daterule

urelativedelta provides a **`daterule`** module, containing functions
for creating iterators which reliably generate a collection of dates
at regular intervals.
For example, the following will yield one `date` on the last day of each
month in 2025:

```python
start = date(2025, 1, 31)
rule = daterule.monthly(start, count=12)
# yields 2025-1-31, 2025-2-28, 2025-3-31, 2025-4-30, ...
```

the most general rule is constructed from a relativedelta:
```python
freq = relativedelta(years=1, months=1, days=-1)
rule = daterule.iterator(freq, start, ...)
```

### shift functions

urelativedelta also exposes useful shift functions which are used internally, namely:

- **`shift_months`** to shift a datelike value by a given number of months
- **`shift_years`** to shift a datelike value by a given number of years
- **`with_year`** to shift a datelike value to a given day
- **`with_month`** to shift a datelike value to a given month
- **`with_year`** to shift a datelike value to a given year

## Design decisions and gotchas

We favour simplicity over complexity: we use only the Gregorian calendar and
make no changes e.g. for dates before the 1500s. We also don't try to
replicate some of the complex functionality of dateutil: we're mostly
interested in shifting dates by years, months, days etc.

For days between the 1st and 28th, shifting by months has an obvious
unambiguous meaning which we always stick to. One month after Jan 28th is
always Feb 28th. Shifting Feb 28th by another month will give Mar 28th.

When shifting a day that has no equivalent in another month (e.g. asking
for one month after Jan 30th), we first compute the target month, and then if
the corresponding day does not exist in that month, we take the final day of the
month as the result. So, on a leap year, one month after Jan 30th is Feb 29th.

The order of precidence for a `relativedelta` is as follows:

1.  Work out the target month, if shifting by months
2.  If the initial day does not exist in that month, take the final day of the month
3.  Execute any further `timedelta` shifts

So a `relativedelta` of 1 month and 1 day applied to Jan 31st first shifts to the
last day of Feb, and then adds a single day, giving the 1st of Mar. Applying to Jan 30th
gives the same result.

Shifted dates have no _memory_ of the date they were shifted from. Thus if we shift
Jan 31st by one month and obtain Feb 28th, a further shift of one month will be Mar 28th,
_not_ Mar 31st.

This leads us to an interesting point about the `relativedelta`: addition is not
_[associative](https://en.wikipedia.org/wiki/Associative_property)_:

```python
start = date(2020, 1, 31)
delta = relativedelta(months=1)

d1 = (start + delta) + delta
d2 = start + (delta + delta)

assert d1 == date(2020, 3, 29)
assert d2 == date(2020, 3, 31)
```

If you want a series of shifted dates, we advise using the `DateRule`, which takes
account of some of these subtleties:
```python
start = date(2020, 1, 31)
delta = relativedelta(months=1)
rule = DateRule(delta, start)
assert next(rule) == date(2020, 1, 31)
assert next(rule) == date(2020, 2, 29)
assert next(rule) == date(2020, 3, 31)
```
