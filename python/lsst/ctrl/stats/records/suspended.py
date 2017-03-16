#
# LSST Data Management System
# Copyright 2008-2012 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#
from __future__ import absolute_import
from .record import Record


class Suspended(Record):
    """Job was suspended

    The job is still on the computer, but is no longer executing.  This
    is usually for a policy reason, such as an interactive user using the
    computer.

    Parameters
    ----------
    year: `str`
        the year to tag the job with
    lines: list
        the strings making up this record
    """

    def __init__(self, year, lines):
        Record.__init__(self, year, lines)


eventClass = Suspended
eventCode = "010"
