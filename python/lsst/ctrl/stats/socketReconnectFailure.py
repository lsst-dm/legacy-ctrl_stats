from record import Record
class SocketReconnectFailure(Record):
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
        self.reason = lines[1].strip()+";"+lines[2].strip()
