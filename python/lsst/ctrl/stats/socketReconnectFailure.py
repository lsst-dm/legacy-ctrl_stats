from record import Record
class SocketReconnectFailure(Record):
    """
    Remote system call reconnect failure
    The "condor_shadow" and "condor_starter" (which communicate while the
    job runs) were unable to resume contact before the job lease expired.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
        self.reason = lines[1].strip()+";"+lines[2].strip()
