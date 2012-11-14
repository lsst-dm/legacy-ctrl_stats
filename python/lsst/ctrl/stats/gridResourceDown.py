from record import Record
class GridResourceDown(Record):
    """
    Detected Down Grid Resource
    The grid resource that a job is to run on is unavailable.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
