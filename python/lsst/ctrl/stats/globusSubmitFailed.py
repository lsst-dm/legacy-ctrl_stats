from record import Record
class GlobusSubmitFailed(Record):
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
