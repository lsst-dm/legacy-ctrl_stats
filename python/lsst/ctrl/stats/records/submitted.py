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

class Submitted(Record):
    """
    Job submitted
    This event occurs when a user submits a job. It is the first event you
    will see for a job, and it should only occur once.
    """
    def __init__(self, year, lines):
        """
        Constructor
        @param year - the year to tag the job with
        @param lines - the strings making up this record
        """
        Record.__init__(self, year, lines)
        
        pat = r"\<(?P<hostAddr>\d+.\d+.\d+.\d+:\d+.+)\>"

        values = re.search(pat,lines[0]).groupdict()
        ## the submitted host's network address
        self.submitHostAddr = values["hostAddr"]

        if len(lines) > 1:
            pat = "DAG Node: (?P<dagNode>\w+)"
            values = re.search(pat,lines[1]).groupdict()
            ## the DAG node that's being worked on
            self.dagNode = values["dagNode"]
        else:
            self.dagNode = None

    def describe(self):
        """
        @return a string describing the contents of this object
        """
        desc = super(Submitted, self).describe()
        if self.dagNode is None:
            s = "%s condorId=%s" % (self.timestamp, self.condorId)
        else:
            s = "%s condorId=%s dagNode=%s" % (self.timestamp, self.condorId, self.dagNode)
        return s

eventClass = Submitted
eventCode = "000"
