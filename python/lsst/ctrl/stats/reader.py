import sys
import re
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
        file = open(inputFile)

        recordList = RecordList()
        recordLines = []
        while 1:
            lines = file.readlines(100000)
            if not lines:
                break
            for line in lines:
                line = line.rstrip('\n')
                if line == "...":
                    rec = self.classify(recordLines)
                    if rec is not None:
                        recordList.append(rec)
                    else:
                        print "couldn't classify:"
                        print recordLines
                        sys.exit(10)
                    recordLines = []
                else:
                    recordLines.append(line)
        print recordList
        recordList.printGroups()

    def classify(self, lines):
        match = re.search(r'Job submitted from host:', lines[0])
        rec = None
        if match:
            rec = Submitted(lines)
            return rec
        match = re.search(r'Job executing on host:', lines[0])
        if match:
            rec = Executing(lines)
            return rec
        match = re.search(r'Image size of job updated:', lines[0])
        if match:
            rec = Updated(lines)
            return rec
        match = re.search(r'Job terminated.', lines[0])
        if match:
            rec = Terminated(lines)
            return rec
        match = re.search(r'Job disconnected, attempting to reconnect', lines[0])
        if match:
            rec = Disconnected(lines)
            return rec
        match = re.search(r'Job was aborted by the user', lines[0])
        if match:
            rec = Aborted(lines)
            return rec
        match = re.search(r'Job was evicted.', lines[0])
        if match:
            rec = Evicted(lines)
            return rec
        match = re.search(r'Job reconnection failed', lines[0])
        if match:
            rec = ReconnectionFailed(lines)
            return rec
        match = re.search(r'Shadow exception', lines[0])
        if match:
            rec = ShadowException(lines)
            return rec
        match = re.search(r'Job was held', lines[0])
        if match:
            rec = Held(lines)
            return rec
        return  rec
        


if __name__ == "__main__":
    records = Reader(sys.argv[1])
