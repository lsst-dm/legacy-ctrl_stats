from record import Record
class JobRemoteStatusUnknown(Record):
    """
    The job's remote status is unknown
    No updates of the job's remote status have been received for 15 minutes.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
