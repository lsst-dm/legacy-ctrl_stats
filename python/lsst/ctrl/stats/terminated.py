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
class Terminated(Record):
    """
    Job terminated
    The job has completed.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)

        pat = r"\((?P<term>\d+)\) Normal termination \(return value (?P<returnValue>\d+)\)"

        self.term, self.returnValue = self.extractPair(pat, lines[1], "term", "returnValue")

        self.userRunRemoteUsage, self.sysRunRemoteUsage = self.extractUsrSysTimes(lines[2])

        self.userRunLocalUsage,  self.sysRunLocalUsage  = self.extractUsrSysTimes(lines[3])

        self.userTotalRemoteUsage, self.sysTotalRemoteUsage = self.extractUsrSysTimes(lines[4])

        self.userTotalLocalUsage,  self.sysTotalLocalUsage  = self.extractUsrSysTimes(lines[5])

        pat = r"(?P<bytes>\d+) "
        self.runBytesSent = int(self.extract(pat,lines[6], "bytes"))
        self.runBytesReceived = int(self.extract(pat,lines[7], "bytes"))
        self.totalBytesSent = int(self.extract(pat,lines[8], "bytes"))
        self.totalBytesReceived = int(self.extract(pat,lines[9], "bytes"))

        
        pat = r":\s+(?P<usage>\d+)\s+(?P<request>\d+)$"

        self.diskUsage = "-"
        line = lines[12].strip()
        values = re.search(pat,line)
        if values is not None:
            self.diskUsage, self.diskRequest = self.extractPair(pat,line,"usage","request")
        else:
            pat = r":\s+(?P<request>\d+)$"
            self.diskRequest = self.extract(pat,line,"request")

        self.memoryUsage = "-"
        line = lines[13].strip()
        values = re.search(pat,line)
        if values is not None:
            self.memoryUsage, self.memoryRequest = self.extractPair(pat,line,"usage","request")
        else:
            pat = r":\s+(?P<request>\d+)$"
            self.memoryRequest = self.extract(pat,line,"request")


    def printAll(self):
        Record.printAll(self)
        print "term = ",self.term
        print "returnValue = ",self.returnValue
        print "userRunRemoteUsage = ", self.userRunRemoteUsage
        print "sysRunRemoteUsage = ", self.sysRunRemoteUsage
        print "userRunLocaleUsage = ", self.userRunLocalUsage
        print "sysRunLocaleUsage = ", self.sysRunLocalUsage

        print "userTotalRemoteUsage = ", self.userTotalRemoteUsage
        print "sysTotalRemoteUsage = ", self.sysTotalRemoteUsage
        print "userTotalLocalUsage = ", self.userTotalLocalUsage
        print "sysTotalLocalUsage = ", self.sysTotalLocalUsage

        print "runBytesSent ",self.runBytesSent
        print "runBytesReceived ",self.runBytesReceived
        print "totalBytesSent ",self.totalBytesSent
        print "totalBytesReceived ",self.totalBytesReceived

    def describe(self):
        desc = super(Terminated, self).describe()
        s = "%s runUser=%s totalUser=%s" % (self.timestamp, self.userRunRemoteUsage, self.userTotalRemoteUsage)
        return s
