from record import Record
class GridResourceUp(Record):
    """
    Grid Resource Back Up
    A grid resource that was previously unavailable is now available.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
