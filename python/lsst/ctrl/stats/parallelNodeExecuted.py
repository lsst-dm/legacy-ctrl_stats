from record import Record
class ParallelNodeExecuted(Record):
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
