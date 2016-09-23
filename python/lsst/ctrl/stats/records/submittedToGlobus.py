from __future__ import absolute_import
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
from .record import Record

#
#
# 017 (001.000.000) 03/24 19:13:30 Job submitted to Globus
#     RM-Contact: test.ncsa.illinois.edu/jobmanager-fork
#     JM-Contact: https://test.ncsa.illinois.edu:34127/28997/1174763610/
#     Can-Restart-JM: 1
# ...


class SubmittedToGlobus(Record):
    """
    Job submitted to Globus
    A grid job has been delegated to Globus (version 2, 3, or 4).  This event
    is no longer used, but is here for completeness.
    """

    def __init__(self, year, lines):
        """
        Constructor
        @param year - the year to tag the job with
        @param lines - the strings making up this record
        """
        Record.__init__(self, year, lines)

eventClass = SubmittedToGlobus
eventCode = "017"
