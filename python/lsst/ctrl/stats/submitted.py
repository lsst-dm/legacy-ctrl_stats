import re
from record import Record

class Submitted(Record):
    def __init__(self, lines):
        Record.__init__(self,lines)

        
        pat = r"\<(?P<host>\d+.\d+.\d+.\d+:\d+)\>"

        values = re.search(pat,lines[0]).groupdict()
        self.host = values["host"]

        pat = "DAG Node: (?P<dag>\w+)"
        values = re.search(pat,lines[1]).groupdict()
        self.dag = values["dag"]

    def printAll(self):
        Record.printAll(self)
        print "host = ",self.host
        print "dag= ",self.dag
