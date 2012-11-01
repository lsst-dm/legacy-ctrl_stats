import os
import sys
import re
import datetime
from submitted import Submitted
from executing import Executing
from terminated import Terminated
from updated import Updated
from disconnected import Disconnected
from aborted import Aborted
from evicted import Evicted
from reconnectionFailed import ReconnectionFailed
from shadowException import ShadowException
from held import Held
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

    def getRecordList(self):
        return self.recordList

    def classify(self, year, lines):
        match = re.search(r'Job submitted from host:', lines[0])
        rec = None
        if match:
            rec = Submitted(year, lines)
            return rec
        match = re.search(r'Job executing on host:', lines[0])
        if match:
            rec = Executing(year, lines)
            return rec
        match = re.search(r'Image size of job updated:', lines[0])
        if match:
            rec = Updated(year, lines)
            return rec
        match = re.search(r'Job terminated.', lines[0])
        if match:
            rec = Terminated(year, lines)
            return rec
        match = re.search(r'Job disconnected, attempting to reconnect', lines[0])
        if match:
            rec = Disconnected(year, lines)
            return rec
        match = re.search(r'Job was aborted by the user', lines[0])
        if match:
            rec = Aborted(year, lines)
            return rec
        match = re.search(r'Job was evicted.', lines[0])
        if match:
            rec = Evicted(year, lines)
            return rec
        match = re.search(r'Job reconnection failed', lines[0])
        if match:
            rec = ReconnectionFailed(year, lines)
            return rec
        match = re.search(r'Shadow exception', lines[0])
        if match:
            rec = ShadowException(year, lines)
            return rec
        match = re.search(r'Job was held', lines[0])
        if match:
            rec = Held(year, lines)
            return rec
        return  rec
        


if __name__ == "__main__":
    records = Reader(sys.argv[1])
