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

# Parses Executing records of the form:
#
# 001 (244585.000.000) 08/20 13:09:36 Job executing on host: <192.168.1.121:47727>
# ...
#


class Executing(Record):
    """
    Job executing
    A job is running.  It might occur more than once.
    """

    def __init__(self, year, lines):
        """
        Constructor
        @param year - the year to tag the job with
        @param lines - the strings making up this record
        """
        Record.__init__(self, year, lines)

        pat = r"\<(?P<hostAddr>\S+)\>"

        values = re.search(pat, lines[0]).groupdict()
        # internet address of the host
        hostValues = values["hostAddr"].split("?")
        self.executingHostAddr = hostValues[0]

    def describe(self):
        """
        @return a string describing the contents of this object
        """
        s = "%s host=%s" % (self.timestamp, self.executingHostAddr)
        return s


eventClass = Executing
eventCode = "001"
