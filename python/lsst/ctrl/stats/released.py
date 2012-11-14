from record import Record
class Released(Record):
    """
    Job was released
    The job was in the hold state and is to be re-run.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
