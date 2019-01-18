# coding=utf-8
#
# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis-python
#
# Most of this work is copyright (C) 2013-2018 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
#
# END HEADER

"""This module provides ``dateutil`` timezones.

You can use this strategy to make
:py:func:`hypothesis.strategies.datetimes` and
:py:func:`hypothesis.strategies.times` produce timezone-aware values.
"""

from __future__ import division, print_function, absolute_import

import datetime as dt

from dateutil import tz, zoneinfo  # type: ignore

import hypothesis.strategies as st

__all__ = ['timezones']


@st.cacheable
@st.defines_strategy
def timezones():
    # type: () -> st.SearchStrategy[dt.tzinfo]
    """Any timezone in dateutil.

    This strategy minimises to UTC, or the timezone with the smallest offset
    from UTC as of 2000-01-01, and is designed for use with
    :py:func:`~hypothesis.strategies.datetimes`.

    Note that the timezones generated by the strategy may vary depending on the
    configuration of your machine. See the dateutil documentation for more
    information.
    """
    reference_date = dt.datetime(2000, 1, 1)
    tz_names = zoneinfo.get_zonefile_instance().zones

    all_timezones = [tz.UTC]  # type: ignore
    all_timezones += sorted(
        [tz.gettz(t) for t in tz_names],
        key=lambda zone: abs(zone.utcoffset(reference_date))
    )
    return st.sampled_from(all_timezones)
