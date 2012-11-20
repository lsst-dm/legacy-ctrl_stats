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
from record import Record
class Updated(Record):
    """
    Image size of job updated
    An informational event, to update the amount of memory that the job is
    using while running.  It does not reflect the state of the job.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)

        pat = "Image size of job updated: (?P<imageSize>[\d]+)"
        
        self.imageSize = int(self.extract(pat,lines[0], "imageSize"))
        
        self.memoryUsageMb = "0"
        self.residentSetSizeKb = "0"
        if len(lines) == 3:
            pat = "(?P<memoryUsage>[\d]+)"
            self.memoryUsageMb = int(self.extract(pat,lines[1],"memoryUsage"))
            pat = "(?P<residentSetSize>[\d]+)"
            self.residentSetSizeKb = int(self.extract(pat,lines[2],"residentSetSize"))
        else:
            pat = "(?P<residentSetSize>[\d]+)"
            self.residentSetSizeKb = int(self.extract(pat,lines[1],"residentSetSize"))


    def printAll(self):
        print "U",self.lines

    def describe(self):
        s = "%s imageSize=%s" % (self.timestamp, self.imageSize)
        return s
