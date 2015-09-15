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

# Parses Aborted records of the form:
#
# 009 (244585.000.000) 08/20 13:12:55 Job was aborted by the user.
#     via condor_rm (by user srp)
# ...
#
class Aborted(Record):
    """
    Job aborted
    The user canceled the job.
    """
    def __init__(self, year, lines):
        """
        Constructor
        @param year - the year to tag the job with
        @param lines - the strings making up this record
        """
        Record.__init__(self, year, lines)

        ## reason for abort
        self.reason = lines[1].strip()


    def describe(self):
        """
        @return a string describing the contents of this object
        """
        s = "%s %s" % (self.timestamp, self.reason)
        return s

eventClass = Aborted
eventCode = "009"
