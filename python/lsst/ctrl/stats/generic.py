from record import Record
class Generic(Record):
    """
    Generic log event
    Listed in documention as not used, but here for completeness.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
