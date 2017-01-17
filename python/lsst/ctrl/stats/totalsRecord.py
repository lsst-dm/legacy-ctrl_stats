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
from .submissionsRecord import SubmissionsRecord


class TotalsRecord(SubmissionsRecord):
    """Representation of a "totals" SQL table row.

    Note that the names here must match those of the SQL columns.
    """

    def __init__(self, rec):
        SubmissionsRecord.__init__(self, rec)
        # this first time this job was submitted
        self.firstSubmitTime = "0000-00-00 00:00:00"
        # number of bytes sent
        self.totalBytesSent = 0
        # number of bytes received
        self.totalBytesReceived = 0
        # number of times this job was submitted
        self.submissions = 0
        # number of times this job was executed
        self.executions = 0
        # number of shadow exceptions that occurred
        self.shadowException = 0
        # number of times a socket lost occurred
        self.socketLost = 0
        # number of times a socket reconnection failure  occurred
        self.socketReconnectFailure = 0
        # number of times a socket reestablished communication
        self.socketReestablished = 0
        # job was evicted
        self.evicted = 0
        # job was aborted
        self.aborted = 0
        # number of slots this job used (probably because of it being rescheduled)
        self.slotsUsed = 0
        # number of hosts this job used (probably because of it being rescheduled)
        self.hostsUsed = 0
        # the name of the slot that was last used
        self.slotName = None
