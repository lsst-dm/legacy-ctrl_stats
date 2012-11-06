from record import Record
class ExecutableError(Record):
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)

    def printAll(self):
        print "E",self.lines
