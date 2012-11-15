import MySQLdb
from submissionsRecord import SubmissionsRecord

class TotalsRecord(SubmissionsRecord):
    def __init__(self, rec):
        NodesRecord.__init__(self, rec)
        self.firstSubmitTime = "0000-00-00 00:00:00"
        self.totalBytesSent = 0
        self.totalBytesReceived = 0
        self.totalSubmitting = 0
        self.totalExecuting = 0
        self.totalShadowException = 0
        self.totalSocketLost = 0
        self.totalSocketReestablished = 0
        self.totalSocketReconnectionFailure = 0
        self.totalSlotsUsed = 0
        self.totalHostsUsed = 0
