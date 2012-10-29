import re
from record import Record
# TODO: check for other cases of this, and handle this better
class ReconnectionFailed(Record):
    def __init__(self, lines):
        Record.__init__(self,lines)
        self.reason = lines[1]
        self.reason2 = lines[2]

    def printAll(self):
        Record.printAll(self)
        print "reason = ",self.reason
        print "reason2 = ",self.reason2
