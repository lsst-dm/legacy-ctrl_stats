import os
import sys
import re
import datetime
from condorEvents import CondorEvents
from recordList import RecordList

class Reader(object):
    def __init__(self, inputFile):
        self.recordList = RecordList()
        recordLines = []

        t = os.path.getmtime(inputFile)
        fileModified = datetime.datetime.fromtimestamp(t)
        # For some reason, condor doesn't put the year on the date,
        # so the nearest guess we can make is by looking at the file modified
        # info, and use that year.
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
        return self.recordList.getRecords()

    def classify(self, year, lines):
        pat = r"(?P<event>\d\d\d)"
        values = re.search(pat,lines[0]).groupdict()
        eventNumber = values["event"]

        if eventNumber in CondorEvents.events:
            recType = CondorEvents.events[eventNumber]
            rec = recType(year, lines)
            return rec
        else:
            return None

if __name__ == "__main__":
    records = Reader(sys.argv[1])
