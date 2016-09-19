from __future__ import absolute_import
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
from .record import Record

# Parses Updated records of the form:
#
# 006 (244585.000.000) 08/20 13:12:55 Image size of job updated: 983888
#     41  -  MemoryUsage of job (MB)
#     41032  -  ResidentSetSize of job (KB)
# ...
#


class Updated(Record):
    """
    Image size of job updated
    An informational event, to update the amount of memory that the job is
    using while running.  It does not reflect the state of the job.
    """

    def __init__(self, year, lines):
        """
        Constructor
        @param year - the year to tag the job with
        @param lines - the strings making up this record
        """
        Record.__init__(self, year, lines)

        pat = "Image size of job updated: (?P<imageSize>[\d]+)"

        ## size of the image for this job
        self.imageSize = int(self.extract(pat, lines[0], "imageSize"))

        ## memory used by this job in MB
        self.memoryUsageMb = 0
        ## resident size of this job in KB
        self.residentSetSizeKb = 0
        if len(lines) == 3:
            pat = "(?P<memoryUsage>[\d]+)"
            self.memoryUsageMb = int(self.extract(pat, lines[1], "memoryUsage"))
            pat = "(?P<residentSetSize>[\d]+)"
            self.residentSetSizeKb = int(self.extract(pat, lines[2], "residentSetSize"))
        else:
            pat = "(?P<residentSetSize>[\d]+)"
            self.residentSetSizeKb = int(self.extract(pat, lines[1], "residentSetSize"))

    def describe(self):
        """
        @return a string describing the contents of this object
        """
        s = "%s imageSize=%s" % (self.timestamp, self.imageSize)
        return s

eventClass = Updated
eventCode = "006"
