from record import Record
class Checkpointed(Record):
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)

    def printAll(self):
        print "C",self.lines
