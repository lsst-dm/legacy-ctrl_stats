from record import Record
class SocketLost(Record):
    """
    Remote system call socket lost
    The "condor_shadow" and "condor_starter" (which communicate while the
    job runs) have lost contact.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
