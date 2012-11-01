from record import Record
class Updated(Record):
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)

    def printAll(self):
        print "U",self.lines
