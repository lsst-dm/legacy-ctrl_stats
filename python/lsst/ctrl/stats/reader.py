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
from __future__ import print_function
from __future__ import absolute_import
from builtins import object
import os
import sys
import re
import datetime
from .recordList import RecordList
import lsst.ctrl.stats.records
import yaml


class Reader(object):
    """Reads a metrics files, nodes.log file and classifies them into Records

    Parameters
    ----------
    metrics: `str`
        the name of the metrics file to read
    logFile: `str`
        the name of the nodes.log file to read

    """

    def __init__(self, metrics, logFile):
        # RecordList containing all records from the log file
        self.recordList = RecordList()
        recordLines = []

        # For some reason, condor doesn't put the year on the date,
        # so we assum this year.

        metricList = None
        with open(metrics, 'r') as stream:
            try:
                metricList = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                return

        d = datetime.datetime.fromtimestamp(metricList['start_time'])
        startDate = d
        startYear = d.year
        d = datetime.datetime.fromtimestamp(metricList['end_time'])
        endYear = d.year

        year = startYear
        prevDate = None
        for line in open(logFile):
            line = line.rstrip('\n')
            if line == "...":
                rec = self.classify(year, recordLines)
                if rec is not None:
                    self.recordList.append(rec)
                else:
                    print("couldn't classify:")
                    print(recordLines)
                    sys.exit(10)
                recordLines = []
            else:
                recordLines.append(line)

        # if all the records in the same year, we're done
        if startYear == endYear:
            return

        # the records span years, so readjust when we run over the year
        # threshold
        records = self.getRecords()
        for job in self.getRecords():
            jobNumber = job
            jobStates = records[jobNumber]
            previousDate = startDate
            for rec in jobStates:
                currentDate = rec.datetime
                if previousDate != None:
                    if previousDate > currentDate:
                        rec.addYear()
                previousDate = rec.datetime
            

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
        values = re.search(pat, lines[0]).groupdict()
        eventNumber = values["event"]

        if eventNumber in lsst.ctrl.stats.records.byCode:
            rec = lsst.ctrl.stats.records.byCode[eventNumber](year, lines)
            return rec
        else:
            return None

if __name__ == "__main__":
    records = Reader(sys.argv[1], sys.argv[2])
