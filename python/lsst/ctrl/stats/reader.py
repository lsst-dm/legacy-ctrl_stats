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
import os
import sys
import re
import datetime
from recordList import RecordList
import lsst.ctrl.stats.records

class Reader(object):
    """Reads in a Condor log file
    """
    def __init__(self, inputFile):
        """Read a Condor log file, classifying all the records into Record
        objects.
        """
        ## RecordList containing all records from the log file
        self.recordList = RecordList()
        recordLines = []

        # For some reason, condor doesn't put the year on the date,
        # so the nearest guess we can make is by looking at the file modified
        # info, and use that year.
        t = os.path.getmtime(inputFile)
        fileModified = datetime.datetime.fromtimestamp(t)
        year = fileModified.year

        file = open(inputFile)
        while 1:
            lines = file.readlines(100000)
            if not lines:
                break
            for line in lines:
                line = line.rstrip('\n')
                if line == "...":
                    rec = self.classify(year, recordLines)
                    if rec is not None:
                        self.recordList.append(rec)
                    else:
                        print "couldn't classify:"
                        print recordLines
                        sys.exit(10)
                    recordLines = []
                else:
                    recordLines.append(line)

    def getRecords(self):
        """Accessor to a list of all Records
        """
        return self.recordList.getRecords()

    def classify(self, year, lines):
        """classify a group of text lines into Record type
        @param year: the year this file was written.
        @param lines: a group of lines in comprising a record
        @return a record of the type the lines represent
        """

        # all records have an event type;  look that up first, to
        # see what type of object it corresponds to, and hand the
        # parameters to that object, because it will know how to
        # parse itself.

        pat = r"(?P<event>\d\d\d)"
        values = re.search(pat,lines[0]).groupdict()
        eventNumber = values["event"]


        if eventNumber in lsst.ctrl.stats.records.byCode:
            rec = lsst.ctrl.stats.records.byCode[eventNumber](year,lines)
            return rec
        else:
            return None
    
if __name__ == "__main__":
    records = Reader(sys.argv[1])
