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
import re
from record import Record
class Evicted(Record):
    """
    Job evicted from machine
    A job was removed from a machine before it was finished.
    """
    # event number: 004
    def __init__(self, year, lines):
        """
        Constructor
        @param year - the year to tag the job with
        @param lines - the strings making up this record
        """
        Record.__init__(self, year, lines)

        ## reason for eviction
        self.reason = lines[1].strip()



        pat = r"\((?P<term>\d+)\) Job was not checkpointed."

        ## termination code
        self.term = self.extract(pat, lines[1], "term")

        userRunRemoteUsage, sysRunRemoteUsage = self.extractUsrSysTimes(lines[2])
        ## remote user run usage time
        self.userRunRemoteUsage = userRunRemoteUsage
        ## remote sys run usage time
        self.sysRunRemoteUsage = sysRunRemoteUsage

        userRunLocalUsage, sysRunLocalUsage  = self.extractUsrSysTimes(lines[3])

        ## local user run usage time
        self.userRunLocalUsage = userRunLocalUsage
        ## local sys run usage time
        self.sysRunLocalUsage  = sysRunLocalUsage

        pat = r"(?P<bytes>\d+) "
        ## bytes sent during the run
        self.runBytesSent = int(self.extract(pat,lines[4], "bytes"))
        ## bytes received during the run
        self.runBytesReceived = int(self.extract(pat,lines[5], "bytes"))


        diskUsage, diskRequest = self.extractUsageRequest(lines[8])
        ## disk used
        self.diskUsage = diskUsage
        ## disk requested
        self.diskRequest = diskRequest

        memoryUsage, memoryRequest = self.extractUsageRequest(lines[9])
        ## memory used
        self.memoryUsage = memoryUsage
        ## memory requested
        self.memoryRequest = memoryRequest

    def describe(self):
        """
        @return a string describing the contents of this object
        """
        s = "%s reason=%s" % (self.timestamp, self.reason)
        return s


eventClass = Evicted
eventCode = "004"
