"""Implements a relativedelta extending python's timedelta with months and years."""
from __future__ import annotations

from datetime import date as _date, datetime as _datetime, timedelta as _pytimedelta
from typing import TYPE_CHECKING as _TYPE_CHECKING

from .utils import shift_months as _shift_months

if _TYPE_CHECKING:
    from typing import Any, TypeVar

    D = TypeVar("D", _datetime, _date)


_ZERO = _pytimedelta(0)


class RelativeDelta:
    """Represents relative difference between two dates."""

    def __init__(
        self,
        years: int = 0,
        months: int = 0,
        timedelta: _pytimedelta | None = None,
        **delta_kwargs,
    ):
        self.total_months = months + 12 * years
        if delta_kwargs:
            self.timedelta = _pytimedelta(**delta_kwargs)
            if timedelta is not None:
                self.timedelta += timedelta
        elif timedelta is not None:
            self.timedelta = timedelta
        else:
            self.timedelta = _ZERO

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
            return (
                self.total_months == other.total_months
                and self.timedelta == other.timedelta
            )
        elif isinstance(other, _pytimedelta):
            return self.total_months == 0 and self.timedelta == other
        else:
            return False

    def __hash__(self):
        return hash((self.total_months, self.timedelta))

    def __bool__(self) -> bool:
        return bool(self.total_months or self.timedelta)

    def __neg__(self) -> RelativeDelta:
        return self.__class__(months=-self.total_months, timedelta=-self.timedelta)

    def __add__(self, other: Any) -> RelativeDelta:
        return self.__radd__(other)

    def __radd__(self, other):
        if isinstance(other, (_date, _datetime)):
            if self.total_months:
                other = _shift_months(other, self.total_months)
            if self.timedelta:
                other += self.timedelta
            return other
        elif isinstance(other, RelativeDelta):
            months = self.total_months + other.total_months
            delta = self.timedelta + other.timedelta
            return self.__class__(months=months, timedelta=delta)
        elif isinstance(other, _pytimedelta):
            months = self.total_months
            delta = self.timedelta + other
            return self.__class__(months=months, timedelta=delta)
        else:
            return NotImplemented

    def __sub__(self, other: Any) -> RelativeDelta:
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __mul__(self, n: int) -> RelativeDelta:
        return self.__class__(
            months=self.total_months * n, timedelta=self.timedelta * n
        )

    def __rmul__(self, n: int) -> RelativeDelta:
        return self * n

    def __floordiv__(self, n: int) -> RelativeDelta:
        return self.__class__(
            months=self.total_months // n, timedelta=self.timedelta // n
        )

    def __repr__(self) -> str:
        return f"relativedelta(months={self.total_months}, timedelta={self.timedelta})"

    def years(self) -> int:
        """Years represented by this delta"""
        return self.total_months // 12

    def months(self) -> int:
        """Months, excluding whole years, represented by this delta"""
        return self.total_months % 12

    def days(self) -> int:
        """Days, excluding months and years, represented by this delta"""
        return self.timedelta.days


relativedelta = RelativeDelta  # XXX: alias for consistency with timedelta and dateutil
