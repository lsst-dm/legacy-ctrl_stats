import re
from record import Record
class Held(Record):
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)

        
        pat = r"Error from (?P<slot>[\w@\d\-.]+): (?P<reason>.+?)($)"
        self.slot, self.reason = self.extractPair(pat,lines[1], "slot", "reason")

        pat = r"Code (?P<code>[\d]+) Subcode (?P<subcode>[\d]+)"
        self.code, self.subcode = self.extractPair(pat,lines[2],"code","subcode")

    def printAll(self):
        Record.printAll(self)
        print ">>slot = ",self.slot
        print ">>reason = ",self.reason
        print ">>code = ",self.code
        print ">>subcode = ",self.subcode
