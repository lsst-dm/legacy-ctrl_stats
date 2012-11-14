from record import Record
class GlobusSubmitFailed(Record):
    """
    Globus submit failed
    The attempt to delegate a job to Globus failed.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
