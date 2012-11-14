import re
from record import Record

class Held(Record):
    """
    Job was held
    The job has transitioned to the hold state.
    This might happen if the user applies the "condor_hold" command to the job.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)

        
        pat = r"Error from (?P<slot>[\w@\d\-.]+): (?P<reason>.+?)($)"
        self.slot, self.reason = self.extractPair(pat,lines[1], "slot", "reason")
        self.reason = self.reason.strip()

        pat = r"Code (?P<code>[\d]+) Subcode (?P<subcode>[\d]+)"
        self.code, self.subcode = self.extractPair(pat,lines[2],"code","subcode")

    def printAll(self):
        Record.printAll(self)
        print ">>slot = ",self.slot
        print ">>reason = ",self.reason
        print ">>code = ",self.code
        print ">>subcode = ",self.subcode
        print ">>timestamp = ",self.timestamp

    def describe(self):
        desc = super(Held, self).describe()
        s = "%s reason=%s" % (self.timestamp, self.reason)
        return s
