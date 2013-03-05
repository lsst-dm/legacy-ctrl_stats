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
import MySQLdb
from submissionsRecord import SubmissionsRecord

class TotalsRecord(SubmissionsRecord):
    """Representation of a "totals" SQL table row.  Note that the names
    here must match those of the SQL columns.
    """
    def __init__(self, rec):
        SubmissionsRecord.__init__(self, rec)
        self.firstSubmitTime = "0000-00-00 00:00:00"
        self.totalBytesSent = 0
        self.totalBytesReceived = 0
        self.submissions = 0
        self.executions = 0
        self.shadowException = 0
        self.socketLost = 0
        self.socketReconnectFailure = 0
        self.socketReestablished = 0
        self.evicted = 0
        self.aborted = 0
        self.slotsUsed = 0
        self.hostsUsed = 0
        self.slotName = None
