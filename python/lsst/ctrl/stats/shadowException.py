import re
from record import Record
class ShadowException(Record):
    def __init__(self, lines):
        Record.__init__(self,lines)

        if lines[1].strip() == pat:
            pat = r"Error from (?P<slot>[\w]+@[\d]+@[\w\-.]+): (?P<reason>[.])($)"
            print "lines[2] = ",lines[2]
            values = self.extractValues(pat,lines[2])
            self.slot = values["slot"]
            self.reason = values["reason"]
        else:
            print "wtf?"
            print "lines[1] = ",lines[1].strip()
            sys.exit(0)

    def printAll(self):
        Record.printAll(self)
        print "slot = ",self.slot
        print "reason = ",self.reason
