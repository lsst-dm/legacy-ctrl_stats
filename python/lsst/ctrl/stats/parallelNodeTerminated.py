from record import Record
class ParallelNodeTerminated(Record):
    """
    Parallel node terminated
    A parallel universe program has completed on a node.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
