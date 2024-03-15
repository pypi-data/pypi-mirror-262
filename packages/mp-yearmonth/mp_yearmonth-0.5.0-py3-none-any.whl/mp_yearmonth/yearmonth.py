# yearmonth.py
# Copyright (c) 2023-2024 Ramon Torres
#
# This module is part of mp-yearmonth and is released under
# the MIT License: https://opensource.org/license/mit/

import re
import calendar
import datetime
from typing import Iterator, Optional, Tuple

_FORMAT_PATTERN = re.compile(r"^(\d{4})-(\d{2})$")


class YearMonth:
    """A class representing a year and month.

    It can represent any month between 0001-01 and 9999-12:

            >>> ym = YearMonth(2021, 1)

    You can use this class to iterate over a range of months:

            >>> start = YearMonth(2021, 1)
            >>> end = YearMonth(2021, 3)
            >>> for ym in YearMonth.range(start, end):
            ...     print(ym)
            2021-01
            2021-02
            2021-03

    You can also add and subtract months:

            >>> ym = YearMonth(2021, 1)
            >>> next_month = ym + 1
            >>> print(next_month)
            2021-02

    Attributes:
        year (int)  : The year.
        month (int) : The month.
    """

    __slots__ = ("_year", "_month")

    def __init__(self, year: int, month: int):
        """Create a new YearMonth object.

        Arguments:
            year: The year.
            month: The month."""
        if not isinstance(year, int):
            raise TypeError("year must be an integer")

        if not isinstance(month, int):
            raise TypeError("month must be an integer")

        if not 1 <= month <= 12:
            raise ValueError("month must be between 1 and 12")

        if not datetime.MINYEAR <= year <= datetime.MAXYEAR:
            raise ValueError(
                f"year must be between {datetime.MINYEAR} and {datetime.MAXYEAR}"
            )

        self._year = year
        self._month = month

    def __str__(self):
        return self.iso8601

    def __repr__(self):
        return f"YearMonth({self.year}, {self.month})"

    def __eq__(self, other):
        if isinstance(other, YearMonth):
            return self.year == other.year and self.month == other.month
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, YearMonth):
            return (self.year, self.month) < (other.year, other.month)
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, YearMonth):
            return (self.year, self.month) <= (other.year, other.month)
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, YearMonth):
            return (self.year, self.month) > (other.year, other.month)
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, YearMonth):
            return (self.year, self.month) >= (other.year, other.month)
        return NotImplemented

    def __hash__(self):
        return hash((self.year, self.month))

    def __add__(self, other) -> "YearMonth":
        if isinstance(other, int):
            return self.applying_delta(other)
        return NotImplemented

    def __sub__(self, other) -> "YearMonth":
        if isinstance(other, int):
            return self.applying_delta(-other)
        return NotImplemented

    def __contains__(self, other) -> bool:
        if isinstance(other, datetime.date) or isinstance(other, datetime.datetime):
            return self.year == other.year and self.month == other.month
        return False

    # Public interface

    @property
    def year(self) -> int:
        """The year."""
        return self._year

    @property
    def month(self) -> int:
        """The month."""
        return self._month

    @property
    def iso8601(self) -> str:
        """The ISO 8601 representation of the year and month."""
        return f"{self.year:04d}-{self.month:02d}"

    @property
    def numdays(self) -> int:
        """The number of days in the month."""
        _, days = calendar.monthrange(self.year, self.month)
        return days

    @property
    def first_day(self) -> datetime.date:
        """Return the first day of the month."""
        return datetime.date(self.year, self.month, 1)

    @property
    def last_day(self) -> datetime.date:
        """Return the last day of the month."""
        return datetime.date(self.year, self.month, self.numdays)

    @classmethod
    def current(cls, tz: Optional[datetime.tzinfo] = None) -> "YearMonth":
        """Return the current year and month.

        Arguments:
            tz: The timezone to use. If None, the system's local timezone is used.
        """
        now = datetime.datetime.now(tz)
        return cls(now.year, now.month)

    @classmethod
    def parse(cls, s: str) -> "YearMonth":
        """Parses a string in the format YYYY-MM into a YearMonth object."""
        match = _FORMAT_PATTERN.match(s)
        if not match:
            raise ValueError(f"Invalid YearMonth string format: {s}")

        year, month = match.groups()
        return cls(int(year), int(month))

    def next(self) -> "YearMonth":
        """Return the next month."""
        if self.month == 12:
            return YearMonth(self.year + 1, 1)
        return YearMonth(self.year, self.month + 1)

    def prev(self) -> "YearMonth":
        """Return the previous month."""
        if self.month == 1:
            return YearMonth(self.year - 1, 12)
        return YearMonth(self.year, self.month - 1)

    def bounds(self) -> Tuple[datetime.date, datetime.date]:
        """Return the first and last day of the month."""
        return (self.first_day, self.last_day)

    def applying_delta(self, months: int) -> "YearMonth":
        """Return the YearMonth that is `months` away from this one."""
        year = self.year + ((self.month + months - 1) // 12)
        month = ((self.month + months - 1) % 12) + 1
        return YearMonth(year, month)

    def distance_to(self, other: "YearMonth") -> int:
        """Return the number of months between this and another YearMonth."""
        return (other.year - self.year) * 12 + (other.month - self.month)

    @classmethod
    def range(cls, start: "YearMonth", end: "YearMonth") -> Iterator["YearMonth"]:
        """Return a list of all months between start and end, inclusive."""
        is_ascending = start <= end
        current = start
        while current != end:
            yield current
            current = current.next() if is_ascending else current.prev()
        yield end
