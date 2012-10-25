import re
from record import Record

class Submitted(Record):
    def __init__(self, lines):
        Record.__init__(self,lines)

        regex = ur"DAG Node: (.+?)$"
        worker = re.findall(regex,lines[1])[0]
        print "worker = ",worker

    def printAll(self):
        print "S",self.lines
