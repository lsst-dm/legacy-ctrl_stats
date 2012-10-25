from record import Record
class Executing(Record):
    def __init__(self, lines):
        Record.__init__(self,lines)

    def printAll(self):
        print "E",self.lines
