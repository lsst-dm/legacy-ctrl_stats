import re
from record import Record
class Aborted(Record):
    """
    Job aborted
    The user canceled the job.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)

        self.reason = lines[1].strip()


    def printAll(self):
        Record.printAll(self)
        print "reason = ",self.reason

    def describe(self):
        s = "%s %s" % (self.timestamp, self.reason)
        return s
