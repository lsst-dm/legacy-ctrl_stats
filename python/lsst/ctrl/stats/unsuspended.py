from record import Record
class Unsuspended(Record):
    """
    Job was unsuspended
    The job has resumed execution, after being suspended earlier.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
