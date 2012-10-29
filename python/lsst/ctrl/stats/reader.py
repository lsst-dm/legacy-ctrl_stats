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

class Reader(object):
    def __init__(self, inputFile):
        file = open(inputFile)

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
                        rec.printAll()
                    else:
                        print "couldn't classify:"
                        print recordLines
                        sys.exit(10)
                    recordLines = []
                else:
                    recordLines.append(line)

    def classify(self, lines):
        print "lines = ",lines
        match = re.search(r'Job submitted from host:', lines[0])
        rec = None
        if match:
            print "Submitted: ",lines[0]
            rec = Submitted(lines)
            return rec
        match = re.search(r'Job executing on host:', lines[0])
        if match:
            print "Executing: ",lines[0]
            rec = Executing(lines)
            return rec
        match = re.search(r'Image size of job updated:', lines[0])
        if match:
            print "Updated: ",lines[0]
            rec = Updated(lines)
            return rec
        match = re.search(r'Job terminated.', lines[0])
        if match:
            print "Terminated: ",lines[0]
            rec = Terminated(lines)
            return rec
        match = re.search(r'Job disconnected, attempting to reconnect', lines[0])
        if match:
            print "Disconnected: ",lines[0]
            rec = Disconnected(lines)
            return rec
        match = re.search(r'Job was aborted by the user', lines[0])
        if match:
            print "Aborted: ",lines[0]
            rec = Aborted(lines)
            return rec
        match = re.search(r'Job was evicted.', lines[0])
        if match:
            print "Evicted: ",lines[0]
            rec = Evicted(lines)
            return rec
        match = re.search(r'Job reconnection failed', lines[0])
        if match:
            print "reconnectionFailed: ",lines[0]
            rec = ReconnectionFailed(lines)
            return rec
        match = re.search(r'Shadow exception', lines[0])
        if match:
            print "shadowException: ",lines[0]
            rec = ShadowException(lines)
            return rec
        return  rec
        


if __name__ == "__main__":
    records = Reader(sys.argv[1])
