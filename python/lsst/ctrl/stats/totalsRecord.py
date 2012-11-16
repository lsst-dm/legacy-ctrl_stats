import MySQLdb
from submissionsRecord import SubmissionsRecord

class TotalsRecord(SubmissionsRecord):
    def __init__(self, rec):
        SubmissionsRecord.__init__(self, rec)
        self.firstSubmitTime = "0000-00-00 00:00:00"
        self.totalBytesSent = 0
        self.totalBytesReceived = 0
        self.submissions = 0
        self.executions = 0
        self.shadowException = 0
        self.socketLost = 0
        self.socketReconnectFailure = 0
        self.socketReestablished = 0
        self.evicted = 0
        self.aborted = 0
        self.slotsUsed = 0
        self.hostsUsed = 0
