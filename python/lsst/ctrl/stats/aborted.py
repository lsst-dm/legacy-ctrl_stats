import re
from record import Record
class Aborted(Record):
    def __init__(self, lines):
        Record.__init__(self,lines)

        #pat = r"removed because (?P<reason>.+?)($)"
        #info = re.search(pat,lines[1])
        #if info is not None:
        #    self.reason = self.extract(pat,lines[1], "reason")
        #else:
        self.reason = lines[1]


    def printAll(self):
        Record.printAll(self)
        print "reason = ",self.reason
