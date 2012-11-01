import re
from record import Record

class Submitted(Record):
    def __init__(self, lines):
        Record.__init__(self,lines)

        
        pat = r"\<(?P<hostAddr>\d+.\d+.\d+.\d+:\d+)\>"

        values = re.search(pat,lines[0]).groupdict()
        self.hostAddr = values["hostAddr"]

        pat = "DAG Node: (?P<dagNode>\w+)"
        values = re.search(pat,lines[1]).groupdict()
        self.dagNode = values["dagNode"]

    def printAll(self):
        Record.printAll(self)
        print "hostAddr = ",self.hostAddr
        print "dagNode = ",self.dagNode
