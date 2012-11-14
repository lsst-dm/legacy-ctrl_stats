from record import Record
class ParallelNodeExecuted(Record):
    """
    Parallel node executed
    A parallel universe program is running on a node.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
