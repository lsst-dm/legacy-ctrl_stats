from record import Record
class SubmittedToGlobus(Record):
    """
    Job submitted to Globus
    A grid job has been delegated to Globus (version 2, 3, or 4).  This event
    is no longer used, but is here for completeness.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
