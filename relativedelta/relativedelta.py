"""Implements a relativedelta extending python's timedelta with months and years."""
from __future__ import annotations

from datetime import date as _date, datetime as _datetime, timedelta as _pytimedelta
from typing import TYPE_CHECKING

from .utils import shift_months

if TYPE_CHECKING:
    from typing import Any


class relativedelta:  # noqa: N801
    def __init__(self, years: int = 0, months: int = 0, timedelta=None, **delta_kwargs):
        self.months = months + 12 * years
        self.timedelta = _pytimedelta(**delta_kwargs)
        if timedelta is not None:
            self.timedelta += timedelta

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, relativedelta):
            return self.months == other.months and self.timedelta == other.timedelta
        elif isinstance(other, _pytimedelta):
            return self.months == 0 and self.timedelta == other
        else:
            return False

    def __hash__(self):
        return hash((self.months, self.timedelta))

    def __bool__(self) -> bool:
        return self.months or self.timedelta

    def __neg__(self) -> relativedelta:
        return type(self)(months=-self.months, timedelta=-self.timedelta)

    def __add__(self, other) -> relativedelta:
        if isinstance(other, relativedelta):
            months = self.months + other.months
            delta = self.timedelta + other.timedelta
        elif isinstance(other, _pytimedelta):
            months = self.months
            delta = self.timedelta + other
        else:
            return NotImplemented

        return self.__class__(months=months, timedelta=delta)

    def __sub__(self, other) -> relativedelta:
        return self + (-other)

    def __radd__(self, other):
        if isinstance(other, (_date, _datetime)):
            return shift_months(other, self.months) + self.timedelta
        elif isinstance(other, (_pytimedelta, relativedelta)):
            return self + other
        else:
            return NotImplemented

    def __rsub__(self, other):
        return other + (-self)

    def __mul__(self, n: int) -> relativedelta:
        return self.__class__(months=self.months * n, timedelta=self.timedelta * n)

    def __floordiv__(self, n: int) -> relativedelta:
        return self.__class__(months=self.months // n, timedelta=self.timedelta // n)

    def __repr__(self) -> str:
        return f"relativedelta(months={self.months}, timedelta={self.timedelta})"
