from record import Record
class SubmittedToGrid(Record):
    """
    Job submitted to grid resource
    A job has been submitted, and is under the auspices of the grid resource.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
