from record import Record
class ExecutableError(Record):
    """
    Error in executable
    The job could not be run because the executable was bad.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)

    def printAll(self):
        print "E",self.lines
