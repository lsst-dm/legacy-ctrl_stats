from record import Record
class Suspended(Record):
    """
    Job was suspended
    The job is still on the computer, but is no longer executing.  This
    is usually for a policy reason, such as an interactive user using the
    computer.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
