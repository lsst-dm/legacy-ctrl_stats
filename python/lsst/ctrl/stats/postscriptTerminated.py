from record import Record
class PostscriptTerminated(Record):
    """
    POST script terminated
    A node in a DAGMan work flow has a script that should be run after a
    job.  The script is run on the submit host.  This event signals that the
    post script has completed.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
