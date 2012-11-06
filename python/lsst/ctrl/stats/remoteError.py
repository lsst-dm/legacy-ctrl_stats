from record import Record
class RemoteError(Record):
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
