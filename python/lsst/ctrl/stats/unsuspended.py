from record import Record
class Unsuspended(Record):
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
