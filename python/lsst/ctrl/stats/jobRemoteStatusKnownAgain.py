from record import Record
class JobRemoteStatusKnownAgain(Record):
    """
    The job's remote status is known again.
    An update has been received for a job whose remote status was previously
    logged as unknown.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
