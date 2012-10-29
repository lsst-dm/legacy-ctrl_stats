import re
from record import Record
class ShadowException(Record):
    def __init__(self, lines):
        Record.__init__(self,lines)

        
        print "lines[1] = ",lines[1]
        pat = r"Error from (?P<slot>[\w]+@[\d]+@[\w\-.]+): (?P<reason>.+?)($)"
        values = self.extractValues(pat,lines[1])
        self.slot = values["slot"]
        self.reason = values["reason"]

    def printAll(self):
        Record.printAll(self)
        print "slot = ",self.slot
        print "reason = ",self.reason
