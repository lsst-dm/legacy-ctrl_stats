from record import Record
class RemoteError(Record):
    """
    Remote error
    The "condor_stater" (which monitors the job on the execution machine) has
    failed.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
