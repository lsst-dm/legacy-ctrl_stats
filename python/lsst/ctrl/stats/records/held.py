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

class Held(Record):
    """
    Job was held
    The job has transitioned to the hold state.
    This might happen if the user applies the "condor_hold" command to the job.
    """
    def __init__(self, year, lines):
        """
        Constructor
        @param year - the year to tag the job with
        @param lines - the strings making up this record
        """
        Record.__init__(self, year, lines)

        
        pat = r"Error from (?P<slot>[\w@\d\-.]+): (?P<reason>.+?)($)"
        slot, reason = self.extractPair(pat,lines[1], "slot", "reason")
        ## slot name
        self.slot = slot
        ## reason job was held
        self.reason = reason.strip()

        pat = r"Code (?P<code>[\d]+) Subcode (?P<subcode>[\d]+)"
        code, subcode = self.extractPair(pat,lines[2],"code","subcode")
        ## error code
        self.code = code
        ## error subcode
        self.subcode = subcode

    def describe(self):
        """
        @return a string describing the contents of this object
        """
        desc = super(Held, self).describe()
        s = "%s reason=%s" % (self.timestamp, self.reason)
        return s

eventClass = Held
eventCode = "012"
