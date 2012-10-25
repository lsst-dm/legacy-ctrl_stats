from record import Record
class Terminated(Record):
    def __init__(self, lines):
        Record.__init__(self,lines)

    def printAll(self):
        print "T",self.lines
