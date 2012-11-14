from record import Record
class SocketReestablished(Record):
    """
    Remote system call socket reestablished
    The "condor_shadow" and "condor_starter" (which communicate while the
    job runs) have been able to resume contact before the job lease expired.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
