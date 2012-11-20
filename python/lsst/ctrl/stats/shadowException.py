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
class ShadowException(Record):
    """
    Shadow exception
    The "condor_shadow", a program on the submit computer taht watches over
    the job and performs some services for the job, failed for some 
    catastrophic reason..  The job will leave the machine and go back into
    the queue.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)

        
        pat = r"Error from (?P<slot>[\w]+@[\d]+@[\w\-.]+): (?P<reason>.+?)($)"
        self.slot = None
        self.reason = None
        self.runBytesSent = None
        self.runBytesReceived = None
        if re.search(pat,lines[1]) is not None:
            values = self.extractValues(pat,lines[1])
            self.slot = values["slot"]
            self.reason = values["reason"].strip()
        else:
            self.reason = lines[1].strip()
            pat = r"(?P<bytes>[\d]+)"
            self.runBytesSent = int(self.extract(pat,lines[2],"bytes"))
            self.runBytesReceived = int(self.extract(pat,lines[3],"bytes"))

    def printAll(self):
        Record.printAll(self)
        print "slot = ",self.slot
        print "reason = ",self.reason
        print "runBytesSent = ",self.runBytesSent
        print "runBytesReceived = ",self.runBytesReceived 
