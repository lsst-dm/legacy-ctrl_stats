import sys
import re
from submitted import Submitted
from executing import Executing
from terminated import Terminated
from updated import Updated

class Reader(object):
    def __init__(self, inputFile):
        file = open(inputFile)

        while 1:
            lines = file.readlines(100000)
            if not lines:
                break
            recordLines = []
            for line in lines:
                line = line.rstrip('\n')
                if line == "...":
                    rec = self.classify(recordLines)
                    rec.printAll()
                    recordLines = []
                else:
                    recordLines.append(line)

    def classify(self, lines):
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
        return  rec
        


if __name__ == "__main__":
    records = Reader(sys.argv[1])
