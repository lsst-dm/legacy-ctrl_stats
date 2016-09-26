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
import re
from .record import Record

# Parses Terminated records of the form:
#
# 005 (254504.000.000) 08/21 10:29:43 Job terminated.
#     (1) Normal termination (return value 0)
#         Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage
#         Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage
#         Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage
#         Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage
#     0  -  Run Bytes Sent By Job
#     0  -  Run Bytes Received By Job
#     0  -  Total Bytes Sent By Job
#     0  -  Total Bytes Received By Job
#     Partitionable Resources :    Usage  Request Allocated
#        Cpus                 :                 1         1
#        Disk (KB)            :        1        1   2148167
#        Memory (MB)          :       10        1       294
# ...
#


class Terminated(Record):
    """
    Job terminated
    The job has completed.
    """

    def __init__(self, year, lines):
        """
        Constructor
        """
        Record.__init__(self, year, lines)

        pat = r"\((?P<term>\d+)\) Normal termination \(return value (?P<returnValue>\d+)\)"

        # the pairs below are split this way because of doxygen complaints
        term, returnValue = self.extractPair(pat, lines[1], "term", "returnValue")
        # termination reason
        self.term = term
        # return value of terminated process
        self.returnValue = returnValue

        userRunRemoteUsage, sysRunRemoteUsage = self.extractUsrSysTimes(lines[2])
        # remote user usage time
        self.userRunRemoteUsage = userRunRemoteUsage
        # remote system usage time
        self.sysRunRemoteUsage = sysRunRemoteUsage

        userRunLocalUsage, sysRunLocalUsage = self.extractUsrSysTimes(lines[3])
        # local user usage time
        self.userRunLocalUsage = userRunLocalUsage
        # local system usage time
        self.sysRunLocalUsage = sysRunLocalUsage

        userTotalRemoteUsage, sysTotalRemoteUsage = self.extractUsrSysTimes(lines[4])
        # total user remote usage time
        self.userTotalRemoteUsage = userTotalRemoteUsage
        # total system remote usage time
        self.sysTotalRemoteUsage = sysTotalRemoteUsage

        userTotalLocalUsage, sysTotalLocalUsage = self.extractUsrSysTimes(lines[5])
        # total user local usage time
        self.userTotalLocalUsage = userTotalLocalUsage
        # total system local usage time
        self.sysTotalLocalUsage = sysTotalLocalUsage

        pat = r"(?P<bytes>\d+) "
        # run bytes sent by job
        self.runBytesSent = int(self.extract(pat, lines[6], "bytes"))
        # run bytes received by job
        self.runBytesReceived = int(self.extract(pat, lines[7], "bytes"))
        # total bytes sent by job
        self.totalBytesSent = int(self.extract(pat, lines[8], "bytes"))
        # total bytes received by job
        self.totalBytesReceived = int(self.extract(pat, lines[9], "bytes"))

        pat = r"Partitionable Resources :\s+Usage\s+\Request\s+Allocated$"

        # disk usage
        self.diskUsage = None

        # disk requested
        self.diskRequest = None

        # memory usage
        self.memoryUsage = None

        # memory requested
        self.memoryRequest = None

        ret = re.search(pat, lines[10])
        if ret is None:
            self.diskUsage, self.diskRequest = self.extractUsageRequest(lines[12])
            self.memoryUsage, self.memoryRequest = self.extractUsageRequest(lines[13])
        else:
            self.diskUsage, self.diskRequest, allocated = self.extractUsageRequestAllocated(lines[12])
            self.memoryUsage, self.memoryRequest, allocated = self.extractUsageRequestAllocated(lines[13])

    def describe(self):
        """
        @return a string describing the contents of this object
        """
        desc = super(Terminated, self).describe()
        if desc is None:
            return None
        s = "%s runUser=%s totalUser=%s" % (
            self.timestamp, self.userRunRemoteUsage, self.userTotalRemoteUsage)
        return s


eventClass = Terminated
eventCode = "005"
