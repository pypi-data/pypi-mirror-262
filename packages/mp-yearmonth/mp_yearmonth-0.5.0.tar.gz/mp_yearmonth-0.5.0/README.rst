mp-yearmonth
============

A year-month datatype for Python.

Installation
------------

.. code-block:: bash

    pip install mp-yearmonth


Usage
-----

.. code-block:: python

    from mp_yearmonth import YearMonth

    ym = YearMonth(2019, 1)
    print(ym) # 2019-01

Getting the current year-month
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    ym = YearMonth.current()


You can also specify a timezone using the `tz` argument:

.. code-block:: python

    import pytz

    ym = YearMonth.current(tz=pytz.timezone("Asia/Tokyo"))


Parsing ISO 8601 strings
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    ym = YearMonth.parse("2019-01")

    print(ym.year) # 2019
    print(ym.month) # 1

Comparing year-months
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    ym1 = YearMonth(2019, 1)
    ym2 = YearMonth(2019, 2)

    print(ym1 == ym2) # False
    print(ym1 < ym2) # True

Adding or subtracting months
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    ym = YearMonth(2019, 1)
    ym += 1

    print(ym) # 2019-02

Iterating over a range of year-months
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    ym1 = YearMonth(2019, 1)
    ym2 = YearMonth(2019, 3)

    for ym in YearMonth.range(ym1, ym2):
        print(ym) # 2019-01, 2019-02, 2019-03

Calculating the distance between two year-months
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    ym1 = YearMonth(2019, 1)
    ym2 = YearMonth(2019, 3)

    distance = ym1.distance_to(ym2) # 2

License
-------

mp-yearmonth is licensed under the MIT license. See `LICENSE <https://github.com/raymondjavaxx/mp-yearmonth/blob/main/LICENSE>`_ for details.
