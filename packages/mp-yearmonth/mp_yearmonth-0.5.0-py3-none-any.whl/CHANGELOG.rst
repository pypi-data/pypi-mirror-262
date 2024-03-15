Changelog
=========

All notable changes to this project will be documented in this file.

v0.5.0
------

-  Added ``YearMonth.first_day`` and ``YearMonth.last_day`` properties to get the first and last day of the month.

v0.4.0
------

-  ``YearMonth.current()`` now accepts a ``tz`` argument to specify the timezone.
-  Made ``YearMonth`` instances immutable.

v0.3.1
------

-  Use ``__slots__`` to optimize memory usage.

v0.3.0
------

-  Added ``YearMonth.distance_to()`` method for calculating the distance between two ``YearMonth`` instances.

v0.2.0
------

-  Added support for membership test operators (`in` and `not in`) for checking if a `date` or `datetime` falls within a `YearMonth`.
-  Improved ``YearMonth.parse()`` performance.

v0.1.0
------

-  Initial release.
