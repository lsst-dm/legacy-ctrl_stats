import sys
import re
from record import Record

class Disconnected(Record):
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)

        
        pat = "Socket between submit and execute hosts closed unexpectedly"

        if lines[1].strip() == pat:
            pat = r"(?P<slot>[\w]+@[\d]+@[\w\-.]+) \<(?P<hostAddr>[\d.:]+)\>"
            values = self.extractValues(pat,lines[2])
            self.slot = values["slot"]
            self.hostAddr = values["hostAddr"]
        else:
            print "unhandled disconnected record fault"
            print "lines[1] = ",lines[1].strip()
            sys.exit(0)

    def printAll(self):
        Record.printAll(self)
        print "slot = ",self.slot
        print "hostAddr = ",self.hostAddr

    def describe(self):
        desc = super(Disconnected, self).describe()
        s = "%s returnValue=%s" % (self.timestamp, self.returnValue)
        return s
