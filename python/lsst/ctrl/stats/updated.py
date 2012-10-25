from record import Record
class Updated(Record):
    def __init__(self, lines):
        Record.__init__(self,lines)

    def printAll(self):
        print "U",self.lines
