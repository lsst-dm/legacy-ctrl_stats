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
        Record.__init__(self, year, lines)

        self.reason = lines[1].strip()



        pat = r"\((?P<term>\d+)\) Job was not checkpointed."

        self.term = self.extract(pat, lines[1], "term")

        self.userRunRemoteUsage, self.sysRunRemoteUsage = self.extractUsrSysTimes(lines[2])

        self.userRunLocalUsage,  self.sysRunLocalUsage  = self.extractUsrSysTimes(lines[3])


        pat = r"(?P<bytes>\d+) "
        self.runBytesSent = int(self.extract(pat,lines[4], "bytes"))
        self.runBytesReceived = int(self.extract(pat,lines[5], "bytes"))


        pat = r":\s+(?P<usage>\d+)\s+(?P<request>\d+)$"

        self.diskUsage = "0"
        self.diskRequest = "0"
        line = lines[8].strip()
        values = re.search(pat,line)
        if values is not None:
            self.diskUsage, self.diskRequest = self.extractPair(pat,line,"usage","request")
        else:
            pat = r":\s+(?P<request>\d+)$"
            self.diskRequest = self.extract(pat,line,"request")

        pat = r":\s+(?P<usage>\d+)\s+(?P<request>\d+)$"
        self.memoryUsage = "0"
        self.memoryRequest = "0"
        line = lines[9].strip()
        values = re.search(pat,line)
        if values is not None:
            self.memoryUsage, self.memoryRequest = self.extractPair(pat,line,"usage","request")
        else:
            pat = r":\s+(?P<request>\d+)$"
            self.memoryRequest = self.extract(pat,line,"request")

    def describe(self):
        s = "%s reason=%s" % (self.timestamp, self.reason)
        return s


eventClass = Evicted
eventCode = "004"
