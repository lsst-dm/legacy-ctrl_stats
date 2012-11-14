from record import Record
class GlobusResourceDown(Record):
    """
    Detected Down Globus Resource
    The Globus resource that a job wants to run on has become unavailable.
    This event is no longer used, but is here for completeness.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
