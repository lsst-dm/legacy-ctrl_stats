from record import Record
class GlobusResourceUp(Record):
    """
    Globus resource up
    The Globus resource that a job wants to run was unavailable, but is
    now available.  This event is no longer used, but is included here
    for completeness.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
