import re
from record import Record

class Executing(Record):
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)

        pat = r"\<(?P<hostAddr>\d+.\d+.\d+.\d+:\d+)\>"

        values = re.search(pat,lines[0]).groupdict()
        self.hostAddr = values["hostAddr"]

    def printAll(self):
        Record.printAll(self)
        print "hostAddr = ",self.hostAddr
