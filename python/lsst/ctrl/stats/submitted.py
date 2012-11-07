import re
from record import Record

class Submitted(Record):
    # event number: 000
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
        
        pat = r"\<(?P<hostAddr>\d+.\d+.\d+.\d+:\d+)\>"

        values = re.search(pat,lines[0]).groupdict()
        self.submitHostAddr = values["hostAddr"]

        pat = "DAG Node: (?P<dagNode>\w+)"
        values = re.search(pat,lines[1]).groupdict()
        self.dagNode = values["dagNode"]

    def printAll(self):
        Record.printAll(self)
        print "submitHostAddr = ",self.submitHostAddr
        print "dagNode = ",self.dagNode

    def describe(self):
        desc = super(Submitted, self).describe()
        s = "%s condorId=%s dagNode=%s" % (self.timestamp, self.condorId, self.dagNode)
        return s

    def fields(self):
        s = "dagNode, condorId"
        return s

    def values(self):
        s = self.dagNode+" "+self.condorId
        return s
