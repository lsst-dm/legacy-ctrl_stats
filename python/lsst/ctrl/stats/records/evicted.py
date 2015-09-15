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

# Parses Evicted records of the form:
#
# 004 (244585.000.000) 08/20 13:12:55 Job was evicted.
#     (0) Job was not checkpointed.
#         Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage
#         Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage
#     0  -  Run Bytes Sent By Job
#     0  -  Run Bytes Received By Job
#     Partitionable Resources :    Usage  Request Allocated
#        Cpus                 :                 1         1
#        Disk (KB)            :        1        1   1347851
#        Memory (MB)          :       41        1       275
# ...
#
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


        pat = r"Partitionable Resources :\s+Usage\s+\Request\s+Allocated$"

        ## disk usage
        self.diskUsage = None

        ## disk requested
        self.diskRequest = None

        ## memory usage
        self.memoryUsage = None

        ## memory requested
        self.memoryRequest = None

        ret = re.search(pat, lines[6])
        if ret is None:
            self.diskUsage, self.diskRequest = self.extractUsageRequest(lines[8])
            self.memoryUsage, self.memoryRequest = self.extractUsageRequest(lines[9])
        else:
            self.diskUsage, self.diskRequest, allocated = self.extractUsageRequestAllocated(lines[8])
            self.memoryUsage, self.memoryRequest, allocated = self.extractUsageRequestAllocated(lines[9])
    

    def describe(self):
        """
        @return a string describing the contents of this object
        """
        s = "%s reason=%s" % (self.timestamp, self.reason)
        return s


eventClass = Evicted
eventCode = "004"
