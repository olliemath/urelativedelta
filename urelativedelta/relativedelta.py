"""Implements a relativedelta extending python's timedelta with months and years."""
from __future__ import annotations

from datetime import date as _date, datetime as _datetime, timedelta as _pytimedelta
from typing import TYPE_CHECKING as _TYPE_CHECKING

from .utils import shift_months as _shift_months

if _TYPE_CHECKING:
    from typing import Any, TypeVar

    D = TypeVar("D", _datetime, _date)


class RelativeDelta:
    """Represents relative difference between two dates."""

    def __init__(
        self,
        years: int = 0,
        months: int = 0,
        timedelta: _pytimedelta | None = None,
        **delta_kwargs,
    ):
        self.months = months + 12 * years
        self.timedelta = _pytimedelta(**delta_kwargs)
        if timedelta is not None:
            self.timedelta += timedelta

    @classmethod
    def difference(cls, d1: D, d2: D) -> RelativeDelta:
        """Create a relativedelta from the difference between two dates.

        This is guaranteed to satisfy
        >>> d2 + RealtiveDelta.between(d1, d2) == d1
        that is, it is the relativedelta equivalent of `d1 - d2`.
        """
        # TODO: optimise this
        months = 12 * (d1.year - d2.year) + (d1.month - d2.month)

        estimate = _shift_months(d2, months)
        if d1 >= d2:
            if estimate > d1:
                months -= 1
                estimate = _shift_months(d2, months)
        else:
            if estimate < d1:
                months += 1
                estimate = _shift_months(d2, months)

        timedelta = d1 - estimate

        return RelativeDelta(months=months, timedelta=timedelta)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, RelativeDelta):
            return self.months == other.months and self.timedelta == other.timedelta
        elif isinstance(other, _pytimedelta):
            return self.months == 0 and self.timedelta == other
        else:
            return False

    def __hash__(self):
        return hash((self.months, self.timedelta))

    def __bool__(self) -> bool:
        return bool(self.months or self.timedelta)

    def __neg__(self) -> RelativeDelta:
        return self.__class__(months=-self.months, timedelta=-self.timedelta)

    def __add__(self, other: Any) -> RelativeDelta:
        if isinstance(other, RelativeDelta):
            months = self.months + other.months
            delta = self.timedelta + other.timedelta
        elif isinstance(other, _pytimedelta):
            months = self.months
            delta = self.timedelta + other
        else:
            return NotImplemented

        return self.__class__(months=months, timedelta=delta)

    def __radd__(self, other):
        if isinstance(other, (_date, _datetime)):
            return _shift_months(other, self.months) + self.timedelta
        elif isinstance(other, (_pytimedelta, RelativeDelta)):
            return self + other
        else:
            return NotImplemented

    def __sub__(self, other: Any) -> RelativeDelta:
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __mul__(self, n: int) -> RelativeDelta:
        return self.__class__(months=self.months * n, timedelta=self.timedelta * n)

    def __floordiv__(self, n: int) -> RelativeDelta:
        return self.__class__(months=self.months // n, timedelta=self.timedelta // n)

    def __repr__(self) -> str:
        return f"relativedelta(months={self.months}, timedelta={self.timedelta})"


relativedelta = RelativeDelta  # XXX: alias for consistency with timedelta and dateutil
