import re
from record import Record
# TODO: check for other cases of this, and handle this better
class ReconnectionFailed(Record):
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
        self.reason = lines[1].strip()
        self.reason2 = lines[2].strip()

    def printAll(self):
        Record.printAll(self)
        print "reason = ",self.reason
        print "reason2 = ",self.reason2

    def describe(self):
        desc = super(Reconnected, self).describe()
        s = "%s reason=%s" % (self.timestamp, self.reason)
        return s
