import re
from record import Record

class Executing(Record):
    def __init__(self, lines):
        Record.__init__(self,lines)

        pat = r"\<(?P<host>\d+.\d+.\d+.\d+:\d+)\>"

        values = re.search(pat,lines[0]).groupdict()
        self.host = values["host"]

    def printAll(self):
        Record.printAll(self)
        print "host = ",self.host
