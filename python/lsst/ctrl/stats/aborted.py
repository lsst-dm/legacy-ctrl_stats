import re
from record import Record
class Aborted(Record):
    def __init__(self, lines):
        Record.__init__(self,lines)

        pat = r"removed because (?P<reason>.+?)($)"

        self.reason = self.extract(pat,lines[1], "reason")


    def printAll(self):
        Record.printAll(self)
        print "reason = ",self.reason
