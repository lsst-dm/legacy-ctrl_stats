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


class SocketReestablished(Record):
    """
    Remote system call socket reestablished
    The "condor_shadow" and "condor_starter" (which communicate while the
    job runs) have been able to resume contact before the job lease expired.
    """

    def __init__(self, year, lines):
        """
        Constructor
        @param year - the year to tag the job with
        @param lines - the strings making up this record
        """
        Record.__init__(self, year, lines)

eventClass = SocketReestablished
eventCode = "023"
