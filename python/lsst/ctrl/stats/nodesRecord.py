import MySQLdb
from dbRecord import DbRecord

class NodesRecord(DbRecord):
    def __init__(self):
        self.condorId = None
        self.dagNode = None
        self.submitTime = None
        self.executionHost = None
        self.executionStartTime = "0000-00-00 00:00:00"
        self.executionStopTime = "0000-00-00 00:00:00"
        self.imageSize = 0
        self.memoryUsageMB = 0
        self.residentSetSize = 0
        self.userRunRemoteUsage = 0
        self.sysRunRemoteUsage = 0
        self.userRunLocalUsage = 0
        self.sysRunLocalUsage = 0
        self.bytesSent = 0
        self.bytesReceived = 0
        self.terminationTime = None
        self.terminationCode = None
        self.terminationReason = None
